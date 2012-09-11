__author__ = 'Alesha'
class element(object):
    def __init__(self,content,weight):
        self.content = content
        self.weight = weight

    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other,element) and self.content == other.content:
            return True
        return False
    def __repr__(self):
        return self.content,self.weight

    def __str__(self):
        return str(self.content)+':'+str(self.weight)
    
    def increment(self,value):
        self.weight += value

    @staticmethod
    def plus(element1,element2):
        if element1.content == element2.content:
            return element(element1.content,element1.weight+element2.weight)

    @staticmethod
    def equals(element1,element2):
        if isinstance(element1,element) and isinstance(element2,element) and element1.content == element2.content and element1.weight == element2.weight:
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
            if i+n_of_gram<=n:
                w_element_left = element(tuple(list_of_words[i:i+n_of_gram]),1)
                left_id = markov_chain.__add(words,w_element_left)
                if i+n_of_gram<n:
                    #virtual right element with 0, because at next step it increment
                    w_element_right = element(tuple(list_of_words[i+1:i+1+n_of_gram]),0)
                    right_id = markov_chain.__add(words,w_element_right)
                    r_element = element((left_id,right_id),1)
                    markov_chain.__add(relations,r_element)

        return words,relations

    @staticmethod
    def __add(list,element):
            if element in list:
                id = list.index(element)
                list_element = list[id]
                list_element.increment(element.weight)
                return id
            else:
                list.append(element)
                return len(list)-1

    def __init__(self,list_of_words,n_of_gram):
        """
        message must be a list of words
        """
        self.n_of_gram = n_of_gram

        self.words,self.relations = markov_chain.__form_elements(list_of_words,n_of_gram)
        self.relations_count = len(list_of_words) - n_of_gram
        self.words_count = self.relations_count + 1

    def append(self,message):
        rel_c = len(message) - self.n_of_gram
        words_c = rel_c+1
        self.words_count += words_c
        self.relations_count +=rel_c
        self.words,self.relations = markov_chain.__form_elements(message,self.n_of_gram,self.words,self.relations)


if __name__ == '__main__':
    mc = markov_chain(['a','b','c','a','b','b','c'],1)
    mc.append(['a','b','c','d '])

#    mc.append(['a','b','c'])
#    mc = markov_chain(['a','b','c','a','b','b','c'],3)