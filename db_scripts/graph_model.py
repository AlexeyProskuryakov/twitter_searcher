# -*- coding: utf-8 -*-

import loggers
from pymorphy.contrib import tokenizers
import tools
import re


__author__ = 'Alesha'
log = loggers.logger

end_of_sentence = re.compile('\w+[\.] ')
big_char = re.compile(u'[A-ZА-Я]+\w+')

#todo 2.2. Метод частотно-контекстной классификации тематики текста
#todo test on the twitter load

#Ничто нас так не характеризует, как наш язык. Наш словарный запас это отражение нашей эрудиции,
#потому насколько изощрены наши языковые обороты, можно сказать, насколько изощрены наши мозги.
#Наша лексика показывает нашу культурную (субкультурную, поколенческую, региональную) принадлежность,
# потому насколько часто мы употребляем те или иные слова, можно сказать, какими темами
# Вы в большей степени интересуетесь, специфические слова выдают специфические интересы.
# На этом можно и замутить алгоритм подбора френдов. На основе близости словаря,
#определять близость интересов и культурного графа, если хотите.
#По используемым оборотам, сложности построения фразы, интеллектуальный уровень пользователя.
#Человек может даже ничего не постить, достаточно будет его комментариев, чтоб подобрать ему собеседника.

#todo do not forget about lapse and approximation
####
#**#
####

#+peoples to this model
#any user is user from cluster of this parameters and cluster of this theme, where we have synonym of hashtag
def get_relation_ttr_users(messages, user_from, user_to):
    """
    returning path with weights in vertices.
    """
    pass


#######################################################
def create_information_element(content):
    """
    it is some piece of information stream. may be it is word content
    """
    return informational_element


def create_people_info_element(content):
    """
    getting peoples by this content/
    or some piece of graph
    """
    return people_info_element


class informational_element(object):
    """
    some information of word about text information stream in which this laying
    """

    def __init__(self, information_stream_info):
        """
        it is may be will: {stream_id, position in stream,
        and another attributes in stream of word (timelines, retweets or another :))))}
        """
        pass


class people_info_element(object):
    def __init__(self, people_class_info):
        """
        some info about peoples {or class of people}
        """


class word(object):
    def __init__(self, content):
        self.informational_element = create_information_element(content)
        self.word = content
        self.peoples_info_element = create_people_info_element(content)

    def set_information_element(self, informational_element):
        self.informational_element = informational_element

    def set_peoples_info_element(self, people_info_element):
        self.peoples_info_element = people_info_element


class text(object):
    def get_path_(self, name):
        return self.__dict__[name]

    def __init__(self, text_content):
        self.content = text_content
        self.min_path = None
        self.words = text.create_words(text_content)
        self.min, self.max, self.words_range = text.calculate_min_and_max_words_count(self.words)

    @staticmethod
    def sift_words(words, sift_patterns=None):
        #todo some wanteds
        """
        #todo create fucking
        create some functionality for sifting words, and excluding some or and not but a is are etc
        """
        return words

    @staticmethod
    def process_words(words):
        #todo some wanteds
        text.sift_words(words)
        return words

    @staticmethod
    def calculate_min_and_max_words_count(words):
        set = tools.create_set_with_counts(words)
        l = int(len(set))
        min = l
        max = 0
        for set_el in set:
            el_count = set_el[1]

            if min > el_count:
                min = el_count
            if max < el_count:
                max = el_count
        return min, max, set

    @staticmethod
    def create_words(sequence):
        if isinstance(sequence, unicode) or isinstance(sequence, str):
            sequence.decode('utf-8', errors='ignore')
            words = tokenizers.extract_tokens(sequence)
            words = text.process_words(words)
            return words

    def get_count_element_unique(self):
        """
        getting count of unique elements in text
        """
        if self.__dict__.has_key('count_u'):
            return self.count_u
        elif self.__dict__.has_key("words_set_c"):
            self.count_u = len(self.words_set_c)
        else:
            self.words_set_c = set(self.words)
            self.count_u = len(self.words_set_c)

        return self.count_u

    def get_count_element_all(self):
        """
        getting count of all element in text
        """
        if self.__dict__.has_key('count_all'):
            return self.count_all
        self.count_all = len(self.words)
        return self.count_all


    def get_count_element(self, element):
        """
        count repeats word in text
        """
        all = self.get_count_element_all()
        count = 0
        positions = []
        for i in range(all):
            if self.words[i] == element:
                count += 1
                positions.append(i)

        return {'count': count, 'positions': positions}

    def get_path_between(self, element, position, pos_left, pos_right):
        """
        for example:
        element a
        position 7
        pos_left 2
        pos_right 3
                  |   `     |
        a,b,c,d,e,f,g,a,f,d,c,e,d,d ;
        return f,g,a,f,d,[c]
        """
        el_position = self.get_count_element(element)
        if not el_position['count']:
            #log.info("for element '%s' not any positions in this text" % element)
            return None
        start = position - pos_left
        stop = position + pos_right
        return [self.words[i] for i in range(start, stop)]

    def get_paths_around(self, node, r=2, exclude=True):
        """
        returning sets of elements around on r of this element and
         on any position of this element
         exclude is exclude this element node

         a, r= 1, exclude = true
         ' |   | ' |   | ' |
         a b c d a b c d a b d c
        """
        log.debug('getting path around element "%s" with radius "%s"' % (node, r))
        el_count = self.get_count_element(node)
        paths = []
        if el_count['count'] > 0:
            for position in el_count['positions']:
                if position + r > self.get_count_element_all() or position - r < 0:
                    continue
                if exclude:
                    path_ = self.words[position + 1:position + r + 1]
                    _path = self.words[(position - r):position]
                    path = _path + path_
                else:
                    path_ = self.words[position + 1:position + r + 1]
                    _path = self.words[position - r:position + 1]
                    path = _path + path_
                paths.append(path)
            return paths
        log.warn('no more elements with this content')
        return None

    def get_path(self, node_start, node_stop, reverse=False):
        """
          -->              -->
        a,b,c,d,e,f,g,a,f,d,c,e,d,d ;
        where start: a and stop g:
         return a,b,c,d,e,f; f,d,c,e,d,d,a,b,c,d,e,f

        if reverse == True:
              <--              <--
        a,b,c,d,e,f,g,a,f,d,c,e,d,d ;
        where start: a and stop g:
        return d,d,e,c,d,f,a; a
        """
        paths = []
        position_start = self.get_count_element(node_start)
        position_stop = self.get_count_element(node_stop)
        if position_start['count'] and position_stop['count']:
            for start_pos in position_start['positions']:
                for stop_pos in position_stop['positions']:
                    if start_pos < stop_pos:
                        path = self.words[start_pos: stop_pos + 1]
                    else:
                        path_ = self.words[start_pos:]
                        _path = self.words[:stop_pos + 1]
                        path = path_ + _path

                    if reverse:
                        path.reverse()

                    paths.append(path)

        else:
            log.info(
                'for elements "%s" and "%s" we can not have some positions in this text' % (node_start, node_stop))
            return None
        return paths


class information_stream(text):
    def __init__(self, text_content, name=None, peoples_info_element=None):
        """
        some realisation of text
        """
        text.__init__(self, text_content)
        self.name = name
        for word in self.words:
            word.set_peoples_info_element(peoples_info_element)
            word.set_information_element(informational_element)


def create_information_streams(content, split_function=None):
    """
    create some list of sequences (sentence) on one big sequence
    may be create graph model from article
    input - list or string of words and some splitter function if it string
    output - list of information stream
    """
    result = []
    #at first - split to sequences by splitter
    if split_function:
        content = split_function(content)
    if isinstance(content, unicode):
    #split on our functionality
        content = content.split(' ')
        buf = []
        result_seq = []
        for i in range(0, len(content) - 1):
            buf.append(content[i])
            if end_of_sentence.match(content[i]) and  big_char.match(content[i + 1]):
                result_seq.append(' '.join(buf))
                buf = []
        content = result_seq
        #it may be string see up or mae be list if list:
    if isinstance(content, list):
        for c_element in content:
            informational_stream = information_stream(c_element)
            result.append(informational_stream)
        return result
        #may be some error - #todo i think about it
    return None


class multi_graph(text):
    """
    it is some wrapper around text and have instances of text
    #todo refactor it is bad practice (no normal form text laying in graph and in informational streams)
    it may be some graph in 
    """

    def __init__(self, content):
        text.__init__(self, content)
        try:
            self.information_streams = create_information_streams(content)
        except Exception as e:
            log.exception(e)
            log.error("why it is not set?")


    def get_words_count(self):
        return self.words_range

    def get_min_max_count_element_in_text(self):
        if self.max and self.min:
            return self.min, self.max

    def get_path_between(self, element, position, pos_left, pos_right):
        """
        returning all paths between element with position and round of left and right
        """
        result = []
        for information_stream in self.information_streams:
            positions = information_stream.get_path_between(element,position,pos_left,pos_right)
            if positions:
                result.append(positions)
        return {'text': text.get_path_between(self, element, position, pos_left, pos_right), 'graph': result}


    #todo realize on graph structure all methods for paths searching
    def get_path(self, node_start, node_stop, reverse=False):
        result = []
        for information_stream in self.information_streams:
            path = information_stream.get_path(node_start,node_stop,reverse)
            if path:
                result.append(path)
        return {'text':text.get_path(node_start,node_stop,reverse),'graph':result}

def thematic_classification_method(text_content, min_word_count, radius ):
    """

    algorithm frequency-context classification/

    create multigraph and fill it
    get all words in range by d(word) (word's count in text in it multigraph)
    get max words in this range
    get detail set on max_words range set (where detail is nearest words at
        multigraph of max words at previous step)


    lapse is n(I)/n(F) is more unicum and less all than lower accurancy of model

    """
    #create multigraph and fill it
    text = multi_graph(text_content)
    #get all words in range by d(word) (word's count in text in it multigraph)
    words = text.get_words_count()
    #get max words in this range
    words = [word for word in words if word[1] >= min_word_count]
    #get detail set on max_words range set (where detail is what around of words in prev step)
    detail_words = [text.get_paths_around(word[0], radius, exclude=True) for word in words]
    detail_words = set(detail_words)


def thematic_range_between_text(text_content, text_founded, radius):
    """
    n - all key elements in s or sf
    s - [] of key elements of text, like k1i,k2i,k3i
    sf - [] of key elements of text_founded
    sum(kn) = 1 if not normal by 1. (sum(ki/n) = 1)

    sigmi = kimin/kimax*ki
    if :
    kimin = ki, kimax = kfi <=> ki < kfi
    kimin = kfi, kimax = ki <=> ki > kfi

    also context:
    f - informational stream of text s
    ff - is of text sf

    get_informational_streams_near_i near belong to r
    i = get_informational_elements from this
    if = also for sf

    fuck off to counts of elements in text we see only occurrence in text

         n# = (if intersect i)*2 / i+if => 0 - less, 1 - more

    sigm  = sum(sigmi)*n#

    """


def searching_values_of_informational_criterion_thematic_of_text(text):
    """
    F: T - > S
        F - function which process T - text to S - thematic words
    S = F(T,param1,param2)
    param1 - threshold of getting S elements
    param2 - radius of analysing informational streams
    params is configurationed and analysing by next function:

    L - T -> int
     L - thematic difference between T1 T2 or S1 and S2

    lapse is:  |Ke - Kc|/Ke
    where ke - L(T1,T2) and kc - L(S1,S2)

    optimal parameters is diff -> 0 where diff is |ke2/ke1 - kc2/kc1|. ke2 is L(T1,T2.2) kc2 is L(T1,T2.2)

    scale = (ke1/kc1 + ke2/kc2)*1/2 ~ ke1/kc2 * how much peoples said about this theme.
    """
