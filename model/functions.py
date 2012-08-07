#-*- coding: utf-8 -*-
import re
import tools

__author__ = '4ikist'

_word_ = 'word'
_hash_tag_ = 'hash_tag'
_url_ = 'url'
_data_ = '_data'

objects = [{'key': 'url', 'value': 0},
        {'key': 'hash_tag', 'value': 1},
        {'key': 'word', 'value': 2},
        {'key':'mention','value':3}] #[url,hash_tag,word,mention]

url_pattern = re.compile('http://[\d\w\.\/]+')
mention_tag_pattern = re.compile('[\@][\d\w]+')
hash_tag_pattern = re.compile('[\#][\d\w]+')

#statistic..............................................................................................................


def __imply_string_obj(input):
    """
    implying string object see objects at up
    """
    if url_pattern.match(input):
        return objects[0]
    if hash_tag_pattern.match(input):
        return objects[1]
    if mention_tag_pattern.match(input):
        return objects[3]
    return objects[2]


def __get_freq(data, element):
    for object_elem in objects:
        key = object_elem['key']
        if element in data[key + _data_]:
            return {'freq_' + key: float(data[key + _data_].count(element)) / data[key], 'entity': element, 'type': key}


#todo rewrite this piece of shit! Stop drink! I not believe that it not contains any bugs!
def __get_statistic_of_tweets(data):
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


def get_hash_tags(text):
    return [tag for tag in hash_tag_pattern.findall(text)]

def get_mention_weight(obj):
    """
    for calculating weights of mentions
    return weight = freq in this type / freq in all
    """
    return float(obj['freq_hash_tag']) / float(obj['freq_all'])


def create_statistic_of_tweets(m_user):
    timeline = tools.flush(m_user.timeline, lambda x:x['text'])
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
    smiles = [el for el in regexp.findall(input) if el and len(el.strip())>1]

    for smile in smiles:
        print smile
        if smile_bad.match(smile):
            count_bad += 1
        elif smile_good.match(smile):
            count_good += 1
        else:
            count_neutral += 1

    return {'good': count_good, 'bad': count_bad, 'neutral': count_neutral}


def extracts_text_elements(text):
    if isinstance(text,str) or isinstance(text,unicode):
        words = text.split()
        return words


if __name__ == '__main__':
#    pass
#    result = __get_statistic_of_tweets(['Just posted a photo http://instagr.am/p/MlV8CDDw3M/',
#                                      '@govnokod Че за хрень. Сколько ждать, когда я выра сту блиать. Отстой ваш говнокод.'])
#    print get_count_smiles('(-: :-)))))')
#
#    for e in result:
#        print e
    print get_hash_tags('@govnokod Че за хрень. Сколько ждать, когда я выра сту блиать. Отстой ваш говнокод. http://instagr.am/p/MlV8CDDw3M/')