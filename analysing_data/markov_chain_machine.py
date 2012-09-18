from operator import mod
from pymongo import ASCENDING
from analysing_data.mc_model import element
from differences.diff_machine import difference_element, difference_factory

import loggers
from model.db import db_handler

__author__ = 'Alesha'

log = loggers.logger


def __form_elements(list_of_words, n_of_gram_=1, words=None, relations=None, add_object=None, model_id_=None):
    if not relations: relations = []
    if not words: words = []

    n = len(list_of_words)
    for i in range(n):
        # at first - left element
        if i + n_of_gram_ <= n:
            w_element_left = element(tuple(list_of_words[i:i + n_of_gram_]), 1,
                                     type=element.w_type,
                                     model_id_=model_id_,
                                     additional_obj=add_object
            )

            left_id = __add(words, w_element_left)
            if i + n_of_gram_ < n:
                #virtual right element with 0, because at next step it increment
                w_element_right = element(tuple(list_of_words[i + 1:i + 1 + n_of_gram_]), 0, type=None)
                right_id = __add(words, w_element_right)
                r_element = element((left_id, right_id), 1, model_id_=model_id_)
                r_element.additional_obj = add_object
                __add(relations, r_element)

    return words, relations


def __add(list, element, ind=lambda x, y:x.index(y), get=lambda x, y:x[y]):
    if element in list:
        id = ind(list, element)
        list_element = get(list, id)
        list_element.increment(element.weight)
        list_element.mc_id = id
        return id
    else:
        id = len(list) - 1
        element.mc_id = id
        list.append(element)
        return id


class markov_chain(object):
    def __init__(self, list_of_words=None, n_of_gram_=1, add_object=None, model_id_=None, db_booster=None):
        """
        note: message must be a list of words.
        input parameters: list of words and n which any node will be at parameter n_of_gram_ms
        for ex: if n_of_gram_ms will be 3 than
        mc of a,b,c,d will be
        (a,b,c),1/2 --- 1 ---> (b,c,d),1/2
        with relations count is len of (list of words) -- n and with plus - is count of words/
        count of unique words/relations see: len(obj.words/relations)
        """
        self.n_of_gram_ = n_of_gram_

        self.relations_count_ = 0
        self.words_count_ = 0

        if list_of_words and n_of_gram_:
            self.words, self.relations = __form_elements(list_of_words, n_of_gram_, add_object=add_object)

            self.relations_count_ = len(list_of_words) - n_of_gram_
            self.words_count_ = self.relations_count_ + 1

        self.model_id_ = model_id_
        self.db_booster = db_booster

    def append(self, message, add_object=None):
        """
        append message at markov chain
        """
        rel_c = len(message) - self.n_of_gram_
        words_c = rel_c + 1
        self.words_count_ += words_c
        self.relations_count_ += rel_c
        self.words, self.relations = __form_elements(message, self.n_of_gram_,
                                                     self.words, self.relations,
                                                     add_object=add_object)

    def _get_relations_by_id(self, id, is_from=0    ):
        relations = []
        for r_element in self.relations:
            if r_element.content[is_from] == id:
                relations.append(r_element)
        return relations

    #user method/
    def get_relations_for_word_content(self, word, is_from=0):
        """
        word is some one word.
        attention!: is_from - if 0 than return relations which have from this word
                    if is_from = 1 into this word.

        for boost with mongo - use

        returning relations of some word. if n > 0 all nodes which contains this word
        like that:
                [{'from': w_from, 'to': w_to, 'weight': weight},...]
        """
        result = []
        for i in range(len(self.words)):
            if word.content == self.words[i].content:
                log.info('find word content for word: %s' % word)
                relations = self._get_relations_by_id(i, is_from)
                result.extend(relations)
        return result


    def get_all_relations(self, word=None, id=None):
        result = []
        if word:
            result.extend(self.get_relations_for_word_content(word, 1))
            result.extend(self.get_relations_for_word_content(word))
        if id:
            result.extend(self._get_relations_by_id(word))
            result.extend(self._get_relations_by_id(word, 1))
        if not word and not id:
            return self.relations
        return result

    def _get_adjacent_elements(self, element, adj_ind=0, words=True, is_from=0, relations=False, rec_adj=0 ):
        elements = []
        if words:
            for relation in self._get_relations_by_id(id=element.mc_id, is_from=is_from):
                elements.append(self.words[relation.content[is_from]])
                log.debug('elements is: [%s]' % ', '.join(elements)[:-1])
                if rec_adj < adj_ind:
                    for element in elements:
                        elements.extend(self._get_adjacent_elements(element,adj_ind=adj_ind,words=words,is_from=is_from,rec_adj=rec_adj+1))

        if relations:
            elements = []
            log.warn('#todo! realize relations in getting a')
            pass

        return set(elements)

    def extend(self, i_markov_chain):
        """
        adding at self markov chain new markov chain
        """
        if i_markov_chain.n_of_gram_ != self.n_of_gram_:
            raise Exception('n of grams is not equals!')

        self.relations_count_ += i_markov_chain.relations_count_
        self.words_count_ += i_markov_chain.words_count_

        #by all words in input markov chain
        for i in range(len(i_markov_chain.words)):
            #get word element and his relations
            word_element = i_markov_chain.words[i]
            relations_from_we = i_markov_chain._get_relations_by_id(i)
            #form id of word element in self context
            new_from_id = __add(self.words, word_element)
            #for relations which from word element, retrieve child elements
            for relation in relations_from_we:
                child_word_element = i_markov_chain.words[relation.content[1]]
                #formning new id for child
                el_for_index = element(child_word_element.content, 0, type=None)
                new_to_id = __add(self.words, el_for_index)
                #and creating new relation element
                new_rel_element = element((new_from_id, new_to_id), relation.weight, type=element.r_type)
                #storing
                __add(self.relations, new_rel_element)


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

    def boost_and_save(self, db_booster=None):
        """
        and also save and export thinks
        """
        if not self.db_booster and not db_booster:
            raise Exception("set db_booster please")
        db_booster.add_mc_element(self.words)
        db_booster.add_mc_element(self.relations)
        db_booster.add_mc_parameters(self)

    @staticmethod
    def load_boosted(model_id_, db_booster=None):
        if not self.db_booster and not db_booster:
            raise Exception("set db_booster please")

        relations = db_booster.get_mc_elements({'type': element.r_type}, model_id_)
        words = db_booster.get_mc_elements({'type': element.w_type}, model_id_)
        head = db_booster.get_mc_parameters(model_id)

        mc = markov_chain()
        mc.relations_count_ = head['relations_count_']
        mc.words_count_ = head['words_count_']

        mc.words = words
        mc.relations = relations
        return mc


    #todo test it!
    @staticmethod
    def get_related_words(words_list, db_booster, model_id_):
        """
        search by words inclusive all intersection with...
        """
        return db_booster.get_mc_elements(by_content={'content': words_list,
                                                      'type': element.w_type},
                                          model_id_=model_id_,
                                          by_list_in_content=False, )


    @staticmethod
    def _create(words, relations):
        m_c = markov_chain()
        m_c.words = words
        m_c.relations = relations

        wc = 0
        rc = 0
        for word in m_c.words:
            wc += word.weight

        for rel in m_c.relations:
            rc += rel.weight

        m_c.relations_count_ = rc
        m_c.words_count_ = wc


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

    @staticmethod
    def _print(mc, print_f):
        print_f('[--nodes of chain--]')
        for el in mc.words:
            print_f(el)

        print_f('[--edges of chain--]')
        for el in mc.relations:
            print_f(
                '%s --- %s --> %s' % (mc.words[el.content[0]].content, el.weight, mc.words[el.content[1]].content))
        print_f('[-----------------]')


