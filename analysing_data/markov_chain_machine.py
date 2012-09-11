import loggers

__author__ = 'Alesha'

log = loggers.logger

class element(object):
    def __init__(self, content, weight):
        self.content = content
        self.weight = weight

    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other, element) and self.content == other.content:
            return True
        return False

    def __repr__(self):
        return self.content, self.weight

    def __str__(self):
        return str(self.content) + ':' + str(self.weight)

    def increment(self, value):
        self.weight += value

    @staticmethod
    def equals(element1, element2):
        if isinstance(element1, element) and isinstance(element2,
                                                        element) and element1.content == element2.content and element1.weight == element2.weight:
            return True
        return False


class markov_chain(object):
    @staticmethod
    def __form_elements(list_of_words, n_of_gram=1, words=None, relations=None):
        if not relations: relations = []
        if not words: words = []

        n = len(list_of_words)
        for i in range(n):
            # at first - left element
            if i + n_of_gram <= n:
                w_element_left = element(tuple(list_of_words[i:i + n_of_gram]), 1)
                left_id = markov_chain.__add(words, w_element_left)
                if i + n_of_gram < n:
                    #virtual right element with 0, because at next step it increment
                    w_element_right = element(tuple(list_of_words[i + 1:i + 1 + n_of_gram]), 0)
                    right_id = markov_chain.__add(words, w_element_right)
                    r_element = element((left_id, right_id), 1)
                    markov_chain.__add(relations, r_element)

        return words, relations

    @staticmethod
    def __add(list, element):
        if element in list:
            id = list.index(element)
            list_element = list[id]
            list_element.increment(element.weight)
            return id
        else:
            list.append(element)
            return len(list) - 1

    def __init__(self, list_of_words, n_of_gram):
        """
        message must be a list of words
        """
        self.n_of_gram = n_of_gram

        self.words, self.relations = markov_chain.__form_elements(list_of_words, n_of_gram)
        self.relations_count = len(list_of_words) - n_of_gram
        self.words_count = self.relations_count + 1

    def append(self, message):
        rel_c = len(message) - self.n_of_gram
        words_c = rel_c + 1
        self.words_count += words_c
        self.relations_count += rel_c
        self.words, self.relations = markov_chain.__form_elements(message, self.n_of_gram, self.words, self.relations)

    def _get_relations(self, word_element, is_from=0):
        """
        also in get_child - if is_from = 0 find by left id of relation, 1 - right
        """
        if word_element in self.words:
            we_id = self.words.index(word_element)
            return self._get_relations_by_id(we_id, is_from)

    def _get_relations_by_id(self, id, is_from=0):
        relations = []
        for r_element in self.relations:
            if r_element.content[is_from] == id:
                relations.append(r_element)
        return relations

    def _prepare_relations(self, relations):
        all_weight = float(0)
        result = []
        #calculate weight
        for relation in relations:
            all_weight += relation.weight

        #form normal relations
        for relation in relations:
            w_from = self.words[relation.content[0]].content
            w_to = self.words[relation.content[1]].content
            weight = float(relation.weight) / all_weight
            result.append({'from': w_from, 'to': w_to, 'weight': weight})
        return result

    def get_relations(self, word, is_from=0):
        result = []
        for i in range(len(self.words)):
            if word in self.words[i].content:
                relations = self._get_relations_by_id(i, is_from)
                result.extend(self._prepare_relations(relations))
        return result


    def extend(self, i_markov_chain):
        if i_markov_chain.n_of_gram != self.n_of_gram:
            raise Exception('n of grams is not equals!')

        self.relations_count += i_markov_chain.relations_count
        self.words_count += i_markov_chain.words_count

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
                el_for_index = element(child_word_element.content, 0)
                new_to_id = markov_chain.__add(self.words, el_for_index)
                #and creating new relation element
                new_rel_element = element((new_from_id, new_to_id), relation.weight)
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

    def export(self):
        #todo create export to mongo, graph and...
        #think at setters and getters. It is very important
        for relation in self.relations:
            pass
            
        
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