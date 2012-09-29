# coding=utf-8

from pymorphy import get_morph
from properties import props

__author__ = '4ikist'

morph_en = get_morph(props.dict_en_path, backend='pickle')
morph_ru = get_morph(props.dict_ru_path, backend='pickle')

excludes_classes = [u'ПРЕДЛ', u'СОЮЗ', u'ЧАСТ', u'ADVERB', u'CONJ', u'PREP']

def tokenize(message):
    words = unicode(message).upper().split()
    return words

def get_words(message):
    """
    message is string.
    returning words
    """
    words = tokenize(message)
    result = []
    for word in words:
        gram_info = morph_en.get_graminfo(word, predict=False)
        if not gram_info:
            gram_info = morph_ru.get_graminfo(word, predict=False)

        if gram_info:
            if gram_info[0]['class'] not in excludes_classes:
                result.append(gram_info[0]['norm'])
        else:
            result.append(word)
    return result




        