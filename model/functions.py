#-*- coding: utf-8 -*-
import re
from model.tw_model import m_hash_dict
import tools

__author__ = '4ikist'

word = 'word'
hash_tag = 'hash_tag'
mention = 'mention'
url = 'url'


url_pattern = re.compile('http://[\d\w\.\/]+')
mention_tag_pattern = re.compile('[\@][\d\w]+')
hash_tag_pattern = re.compile('[\#][\d\w]+')

#statistic..............................................................................................................


def __imply_string_obj(input, types):
    """
    implying string object see objects at up
    """
    if url_pattern.match(input):
        types[url].append(input)
        return
    if hash_tag_pattern.match(input):
        types[hash_tag].append(input)
        return
    if mention_tag_pattern.match(input):
        types[mention].append(input)
        return
    types[word].append(input)


def __get_freq(data, element):
    for object_elem in objects:
        key = object_elem['key']
        if element in data[key + _data_]:
            return {'freq_' + key: float(data[key + _data_].count(element)) / data[key], 'entity': element, 'type': key}


def __get_statistic_of_tweets(data):
    """
    input some [] with strings
    which return [] of {freq :<frequency_of_this_element_in_all_elements_in_input>, type:<type_name>, entity:<word>}
    //also in db - will can create collection entities, which include some interests
    """
    all_data = ' '.join(data)
    all_data = all_data.split()
    types = {mention: [], word: [], hash_tag: [], url: []}

    #separate and implying string types
    for element in all_data:
        __imply_string_obj(element, types)

    #calculate all frequencies:
    result = []
    all_len = float(len(all_data))
    for type, arr in types.items():
        for el in arr:
            result.append(m_hash_dict({'entity': el,
                                       'freq':  float(all_data.count(el))/all_len,
                                       'type': type}))

    return {'statistic': list(set(result)),
            hash_tag: list(set(types[hash_tag])),
            mention: list(set(types[mention]))}


def create_statistic_of_tweets(timeline):
    timeline = tools.flush(timeline, lambda x:x['text'])
    result = __get_statistic_of_tweets(timeline)
    return result

#:{)

smile_regexp = re.compile("[)({}\]\[\*\?@!$%><0O]{0,1}[-=~_]{0,1}[:;o]{0,1}[-=~_]{0,1}[)({}\]\[\*\?@!$%><D0O]{0,1}")
smile_bad = re.compile('(.*[\[\(\{]$)|(^[\)\]\}].*)')
smile_good = re.compile('(.*[\]\)\}D]$)|(^[\(\[\{].*)')

def get_count_smiles(input, regexp=smile_regexp):
    count = 0
    count_good = 0
    count_bad = 0
    count_neutral = 0
    smiles = [el for el in regexp.findall(input) if el and len(el.strip()) > 1]

    for smile in smiles:
        print smile
        if smile_bad.match(smile):
            count_bad += 1
        elif smile_good.match(smile):
            count_good += 1
        else:
            count_neutral += 1

    return {'good': count_good, 'bad': count_bad, 'neutral': count_neutral}




if __name__ == '__main__':
    pass