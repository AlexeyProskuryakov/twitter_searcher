# coding=utf-8

from pymorphy import get_morph
from properties import props
import re
from loggers import logger


log = logger
__author__ = '4ikist'

morph_en = get_morph(props.dict_en_path, backend='pickle')
morph_ru = get_morph(props.dict_ru_path, backend='pickle')

excludes_classes = [u'ПРЕДЛ', u'СОЮЗ', u'ЧАСТ', u'ADVERB', u'CONJ', u'PREP']

split_pattern = re.compile('\s')

url_pattern = re.compile(u'(http|https)://[\d\w\.\/]+')
mention_tag_pattern = re.compile(u'[\@][\d\w]+')
hash_tag_pattern = re.compile(u'[\#][\d\wА-Яа-я]+')

word_ru_pattern = re.compile(u'[А-Яа-я]+')
word_en_pattern = re.compile(u'[A-Za-z]+')

trim_pattern = re.compile(u'[^A-Za-zА-Яа-я0-9]+')


def trim(word):
    """
    trim word for any non word characters left and right
    """
    split_els = trim_pattern.split(word)
    for split_el in split_els:
        if len(split_el):
            return split_el


def tokenize(message):
    """
    returning tokens of input message/ implying hashtags, mentions
    """
    all_tokens = split_pattern.split(message)
    tokens = []

    for i in range(len(all_tokens)):
        token = all_tokens[i]
        if not len(token):
            continue
        #log.debug('token: [%s]' % token)
        #trying to imply url,hashtag,mention
        if url_pattern.match(token):
            tokens.append({'type': 'url', 'content': token})

        elif hash_tag_pattern.match(token):
            tokens.append({'type': 'htag', 'content': token})

        elif mention_tag_pattern.match(token):
            tokens.append({'type': 'htag', 'content': token})
        #if not - implying word
        else:
            word_candidate = trim(token)
            #log.debug('word candidate: [%s]' % word_candidate)
            #if candidate contain chars or digits
            if word_candidate:
                if word_en_pattern.findall(word_candidate) and word_ru_pattern.findall(word_candidate):
                    tokens.append({'type': '?', 'content': token})
                elif word_ru_pattern.match(word_candidate):
                    tokens.append({'type': 'word', 'lang': 'ru', 'content': word_candidate})
                elif word_en_pattern.match(word_candidate):
                    tokens.append({'type': 'word', 'lang': 'en', 'content': word_candidate})
                else:
                    tokens.append({'type': '?', 'content': token})
            else:
                tokens.append({'type': '?', 'content': token})
    return tokens


def normalise(word):
    """
    returning norm form of word element
    input {type:word, lang:[ru,en],content:some_content}
    """
    content = unicode(word['content']).upper()
    gram_info = None
    if word['lang'] == 'en':
        gram_info = morph_en.get_graminfo(content)
    elif word['lang'] == 'ru':
        gram_info = morph_ru.get_graminfo(content)

    if gram_info and gram_info[0]['class'] not in excludes_classes:
        return gram_info[0]['norm'].lower()


def get_words(message,url_generalization = lambda x: x['content'],is_normalise=True):
    """
    message is string.
    returning words
    """
    tokens = tokenize(message)
    result = []
    for token in tokens:
        #log.debug(token)
        if token['type'] == 'word':
            if is_normalise:
                saved = normalise(token)
                if saved:
                    result.append(saved)
            else:
                result.append(token['content'])
        elif token['type'] == 'url':
            result.append(url_generalization(token))
        else:
            result.append(token['content'])

    return result


def __test():
    test_messages = [u'cенcация!!! отправь CMC на ноmер 442451 и получи конфeтку!!!',
                     u'по mеории верoятносmи, вы выйграли миллион рублей',
                     u'@>--->--->--- я тебя люблю!!!',
                     u'ropoq cпиm сейчaс! просыпайся!',
                     u'JIюбовь me4еm по проводам?! А скоро притечет к тебе!',
                     u'прикольно, тут продаются самые лучшие какашки http://holоcost.ru/test',
                     u'#секс #сиськи у нас есть плюшки! Отправляйте нам деньги!!!   ']

    for message in test_messages:
        log.info("\n\n\tfor message: %s" % message)
        for word in get_words(message,url_generalization=lambda x:'url',is_normalise=True):
            log.info(word)
            #log.info('%s  [%s] %s' % (word['content'], word['type'], word['lang']if word.has_key('lang') else '' ))

if __name__ == '__main__':
    __test()