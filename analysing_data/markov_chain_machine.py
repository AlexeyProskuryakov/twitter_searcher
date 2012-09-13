from operator import mod
from pymongo import ASCENDING
from differences.diff_machine import difference_element,difference_factory

import loggers
from model.db import db_handler

__author__ = 'Alesha'

log = loggers.logger


class element(object):
    r_type = 'r'
    w_type = 'w'

    def __init__(self, content, weight,type,additional_obj = None,model_id_ = None,mc_id= None):
        """
        element which contain some content: if it node - n_gram of words, if it edge - from ind to ind
        weight - some his weight
        also additional object - added in message - some index of message, may be attribute that it was re tweet or another
        """
        self.content = content
        self.weight = weight

        self.f_weight = None
        self.f_rel_weight = None

        self.additional_obj = additional_obj
        #id of markov chain object
        self.model_id_ = model_id_
        #id in words or relation list
        self.mc_id = mc_id
        #id for mongo
        self.type = type
        
    def generate_mongo_id(self):
        self.__id = hash(content)+hash(weight)+hash(additional_obj)+hash(self.model_id_) if self.model_id_ else 31 + hash(mc_id) if self.mc_id else 42 + hash(self.type)
            
        
    def _get_id(self):
        return self.__id
    
    def _set_id(self,id):
        self.__id = id
        
    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other, element) and self.content == other.content and self.additional_obj == other.additional_obj:
            return True
        return False

    def __repr__(self):
        return self.content, self.weight

    def __str__(self):
        return str(self.content) + ':' + str(self.weight)

    def increment(self, value):
        self.weight += value

    def _serialise(self):
        self.generate_mongo_id()
        return self.__dict__

    @staticmethod
    def create(dict):
        el = element(dict['content'],dict['weight'],dict['additional_obj'])
        return el

    @staticmethod
    def equals(element1, element2):
        if isinstance(element1, element) and isinstance(element2,element) and element1.__dict__ == element2.__dict__ :
            return True
        return False


class markov_chain(object):
    
    db_booster = None
    
    @staticmethod
    def __form_elements(list_of_words, n_of_gram=1, words=None, relations=None,add_object=None, model_id_ = None):
        if not relations: relations = []
        if not words: words = []

        n = len(list_of_words)
        for i in range(n):
            # at first - left element
            if i + n_of_gram <= n:
                w_element_left = element(tuple(list_of_words[i:i + n_of_gram]), 1,
                                         type=element.w_type,
                                         model_id_ = model_id_,
                                         additional_obj=add_object
                )


                left_id = markov_chain.__add(words, w_element_left)
                if i + n_of_gram < n:
                    #virtual right element with 0, because at next step it increment
                    w_element_right = element(tuple(list_of_words[i + 1:i + 1 + n_of_gram]), 0,type=None)
                    right_id = markov_chain.__add(words, w_element_right)
                    r_element = element((left_id, right_id), 1,model_id_ = model_id_)
                    r_element.additional_obj = add_object
                    markov_chain.__add(relations, r_element)

        return words, relations

    @staticmethod
    def __add(list, element, ind = lambda x,y:x.index(y), get = lambda x,y:x[y]):
        if element in list:
            id = ind(list,element)
            list_element = get(list,id)
            list_element.increment(element.weight)
            list_element.mc_id = id
            return id
        else:
            id = len(list) - 1
            element.mc_id = id
            list.append(element)
            return id

    def __init__(self, list_of_words = None, n_of_gram= None,add_object = None, model_id_=None,db_booster=None):
        """
        note: message must be a list of words.
        input parameters: list of words and n which any node will be at parameter n_of_gramms
        for ex: if n_of_gramms will be 3 than
        mc of a,b,c,d will be
        (a,b,c),1/2 --- 1 ---> (b,c,d),1/2
        with relations count is len of (list of words) -- n and with plus - is count of words/
        count of unique words/relations see: len(obj.words/relations)
        """
        self.n_of_gram = n_of_gram

        if list_of_words and n_of_gram:
            self.words, self.relations = markov_chain.__form_elements(list_of_words, n_of_gram,add_object=add_object)
            self.relations_count_ = len(list_of_words) - n_of_gram
            self.words_count_ = self.relations_count_ + 1


        self.model_id_ = model_id_
        markov_chain.db_booster = db_booster

    def append(self, message,add_object = None):
        """
        append message at markov chain
        """
        rel_c = len(message) - self.n_of_gram
        words_c = rel_c + 1
        self.words_count_ += words_c
        self.relations_count_ += rel_c
        self.words, self.relations = markov_chain.__form_elements(message, self.n_of_gram,
                                                                  self.words, self.relations,
                                                                  add_object = add_object)


    def get_all_relations(self,word = None,id = None):
        result = []
        if word:
            result.extend(self.get_relations_for_word(word,1))
            result.extend(self.get_relations_for_word(word))
        if id:
            result.extend(self._get_relations_by_id(word))
            result.extend(self._get_relations_by_id(word,1))
        return result

    def _get_relations_by_id(self, id, is_from=0    ):
        relations = []
        for r_element in self.relations:
            if r_element.content[is_from] == id:
                relations.append(r_element)
        return relations

    #deprecated only for visual/
    @staticmethod
    def _prepare_relations(self, relations):
        """
        for relations outgoings or ingoings into some node.
        not for all
        """
        all_weight = float(0)
        result = []
        #calculate weight
        for relation in relations:
            all_weight += relation.weight

        #form normal relations
        for relation in relations:
            w_from = self.words[relation.content[0]]
            w_to = self.words[relation.content[1]]
            weight = float(relation.weight) / all_weight
            result.append({'from': w_from, 'to': w_to, 'weight': weight})
        return result

    #user method/
    def get_relations_for_word(self, word, id=None,is_from=0):
        """
        word is some one word.
        attention!: is_from - if 0 than return relations which have from this word
                    if is_from = 1 into this word.

        for boost with mongo - use get_related_words

        returning relations of some word. if n > 0 all nodes which contains this word
        like that:
                [{'from': w_from, 'to': w_to, 'weight': weight},...]
        """
        result = []
        for i in range(len(self.words)):
            if word in self.words[i].content:
                relations = self._get_relations_by_id(i, is_from)
                result.extend(relations)
        return result

    def extend(self, i_markov_chain):
        """
        adding at self markov chain new markov chain
        """
        if i_markov_chain.n_of_gram != self.n_of_gram:
            raise Exception('n of grams is not equals!')

        self.relations_count_ += i_markov_chain.relations_count_
        self.words_count_ += i_markov_chain.words_count_

        #by all words in input markov chain
        for i in range(len(i_markov_chain.words)):
            #get word element and his relations
            word_element = i_markov_chain.words[i]
            relations_from_we = i_markov_chain._get_relations_by_id(i)
            #form id of word element in self context
            new_from_id = markov_chain.__add(self.words, word_element)
            #for relations which from word element, retrieve child elements
            for relation in relations_from_we:
                child_word_element = i_markov_chain.words[relation.content[1]]
                #formning new id for child
                el_for_index = element(child_word_element.content, 0,type=None)
                new_to_id = markov_chain.__add(self.words, el_for_index)
                #and creating new relation element
                new_rel_element = element((new_from_id, new_to_id), relation.weight,type=element.r_type)
                #storing
                markov_chain.__add(self.relations, new_rel_element)


    def _print(self, print_f):
        print_f('[--nodes of chain--]')
        for el in self.words:
            print_f(el)

        print_f('[--edges of chain--]')
        for el in self.relations:
            print_f('%s --- %s --> %s'%(self.words[el.content[0]].content,el.weight,self.words[el.content[1]].content))
        print_f('[-----------------]')

    def _serialise(self):
        """
        serialising only xxx_ fields
        """
        dict = self.__dict__
        ser_dict = {}
        for dict_el in dict.items():
            if str(dict_el[0]).endswith('_'):
                ser_dict[dict_el[0]] = dict_el[1]
        return ser_dict

    def boost(self,db_booster = None):
        """
        and also save and export thinks
        """
        if not self.db_booster and not db_booster:
            raise Exception("set db_booster please")
        db_booster.add_mc_element(self.words)
        db_booster.add_mc_element(self.relations)
        db_booster.add_mc_parameters(self)

    @staticmethod
    def load(model_id_ ,db_booster = None):
        if not self.db_booster and not db_booster:
            raise Exception("set db_booster please")

        relations = db_booster.get_mc_elements({'type':element.r_type},model_id)
        words = db_booster.get_mc_elements({'type':element.w_type},model_id)
        head = db_booster.get_mc_parameters(model_id)

        mc = markov_chain()
        mc.relations_count_ = head['relations_count_']
        mc.words_count_ = head['words_count_']

        mc.words = words
        mc.relations = relations
        return mc



#todo test it!
    @staticmethod
    def get_relations_of_words(words_list,db_booster,model_id_):
        """
        search by words inclusive all intersection with...
        """
        words = tuple(words_list)
        mc = markov_chain.load(model_id_,db_booster)
        mc.relations = db_booster.get_mc_elements({})


    @staticmethod
    def _create(words,relations):
        m_c = markov_chain()
        m_c.words = words
        m_c.relations = relations

        wc = 0
        rc = 0
        for word in m_c.words:
             wc+=word.weight

        for rel in m_c.relations:
            rc+=rel.weight

        m_c.relations_count_ = rc
        m_c.words_count_ =  wc





if __name__ == '__main__':
    mc = markov_chain(['a', 'b', 'a', 'c'], 1)
    mc.append(['a', 'b', 'c', 'd'])

    mc._print(log.info)

    mc1 = markov_chain(['c', 'd', 'c', 'e'], 1)
    mc1.append(['a', 'b', 'c', 'd'])

    mc1._print(log.info)

    mc.extend(mc1)
    print 'extend:'
    mc._print(log.info)

    print mc.get_relations('a')
#    mc.append(['a','b','c'])
#    mc = markov_chain(['a','b','c','a','b','b','c'],3)