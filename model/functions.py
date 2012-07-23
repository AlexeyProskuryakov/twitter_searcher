#-*- coding: utf-8 -*-
import re

__author__ = '4ikist'

_word_ = 'word'
_hash_tag_ = 'hash_tag'
_url_ = 'url'
_data_ = '_data'

objects = [{'key': 'url', 'value': 0},
        {'key': 'hash_tag', 'value': 1},
        {'key': 'word', 'value': 2}] #[url,hash_tag,word]

url_pattern = re.compile('^http://[\d\w\.\/]+')
hash_tag_pattern = re.compile('^[\#\@][\d\w]+')

#statistic..............................................................................................................


def __imply_string_obj(input):
    if url_pattern.match(input):
        return objects[0]
    if hash_tag_pattern.match(input):
        return objects[1]
    return objects[2]


def __get_freq(data, element):
    for object_elem in objects:
        key = object_elem['key']
        if element in data[key + _data_]:
            return {'freq_' + key: float(data[key + _data_].count(element)) / data[key], 'entity': element, 'type': key}


#todo rewrite this piece of shit! Stop drink! I not believe that it not contains any bugs!
def get_statistic_of_tweets(data):
    """
    input some [] with strings
    which return [] of {freq_word :<frequency_of_this_word_in_all_words_which_have_this_type>, type:<type_name>,
                        freq_all: <frequency_of_this_word_in_words>, entity:<word>}
    //also in db - will can create collection entities, which include some interests
    """
    all_data = ' '.join(data)
    all_data = all_data.split()

    counts = {}
    for object_element in objects:
        key = object_element['key']
        counts[key + _data_] = [elem for elem in all_data  if __imply_string_obj(elem)['key'] == key]
        counts[key] = len(counts[key + _data_])

    count_all = len(all_data)

    data_set = set(
        [(elem, float(all_data.count(elem)) / count_all) for elem in all_data])

    data_set_model = [__get_freq(counts, element[0]) for element in data_set]
    data_set = map(lambda x:{'entity': x[0], 'freq_all': x[1]}, data_set)
    return [dict(data_set[i].items() + data_set_model[i].items()) for i in range(len(data_set))]
#todo rewrite this piece of shit! Stop drink! I not believe that it not contains any bugs!

def get_mention_weight(obj):
    """
    for calculating weights of mentions
    return weight = freq in this type / freq in all
    """
    return float(obj['freq_hash_tag'])/float(obj['freq_all'])




if __name__ == '__main__':
    result = get_statistic_of_tweets(['Just posted a photo http://instagr.am/p/MlV8CDDw3M/',
                               '@govnokod Че за хрень. Сколько ждать, когда я выра сту блиать. Отстой ваш говнокод.'])

    for e in result:
        print e
