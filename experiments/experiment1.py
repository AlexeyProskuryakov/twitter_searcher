# coding=utf-8
import os
from analysing_data.booster import db_mc_handler
from analysing_data.markov_chain_machine import markov_chain
from db_scripts.twitter_timeline_parser import extract_messages
import loggers
from model.db import db_handler
from search_engine import engines
import tools
from text_proc.text_processing import get_words
from analysing_data.mc_difference_logic import diff_markov_chains
import visualise.vis2d_machine as vis

__author__ = '4ikist'
__doc__ = """
Эксперимент 1.
1) Создание общей модели определенного класса людей.
2) Нахождение весов людей на основе принадлежности ленты определенного человека к общей модели.
3) Класстеризация на людей на основе разницы

"""
log = loggers.logger

main_db = db_handler()
engine = engines.tweepy_engine(out=main_db)

booster = db_mc_handler()


def get_users(filename):
    """
    forming users some from db or scrapping from ttr
    """
    result = []
    users = open(filename).readlines()
    for user in users:
        name_ = tools.imply_dog(user, with_dog=True).strip()
        log.info('find user by name "%s"' % name_)
        m_user = main_db.get_user({'name_': name_})
        if m_user:
            log.info('user found %s' % m_user.name_)
            result.append(m_user)
        else:
            log.info('user will load %s' % name_)
            m_user = engine.scrap(name_, neighbourhood=0)
            result.append(m_user)
    return result


def create_model(user, is_normalise=True, mc=None):
    """
    creating model for one user
    """
    if not mc:
        mc = markov_chain(user.name_, booster)

    timeline_text = tools.flush(user.timeline, lambda x:x['text'])

    for tt_el in timeline_text:
        mc.add_message(get_words(tt_el), is_normalise)

    mc.save()
    return mc


def create_model_main(users, model_id, is_normalise=True):
    """
    creating markov chain model for users text
    """
    mc = markov_chain(model_id, booster)
    for m_user in users:
        timeline_text = tools.flush(m_user.timeline, lambda x:x['text'])
        for timeline_text_el in timeline_text:
            message = get_words(timeline_text_el, is_normalise=is_normalise)
            mc.add_message(message)
    mc.save()
    return mc


def little_differences():
    #todo create graph differences between normal and not normal
    path = os.path.dirname(__file__)
    file_name = os.path.join(path, 'no_spam_names')

    #load users
    users = get_users(file_name)

    #create model
    log.info('create main model')
    model = create_model_main(users, 'no_spam', is_normalise=False)
    model_norm = create_model_main(users, 'no_spam_normal', is_normalise=True)
    #model = markov_chain.create('no_spam', booster)

    log.info('create models for any user')
    result = []
    for user in users:
        log.info('create model for user: %s' % user.name_)
        if not user.timeline_count or not len(user.timeline):
            continue
        user_model_normal = create_model(user)
        user_model = create_model(user, is_normalise=False)
        log.info('calculate differences between main model and user model')
        diff_element = diff_markov_chains(user_model_normal, model)
        diff_element_normal = diff_markov_chains(user_model_normal, model_norm)
        log.info('the difference between main model and user model (%s) model is: %s ' % (user.name_, diff_element))

        nodes, edges = model_norm.get_unique_nodes_edges()
        result.append({'user': user.name_, 'x': diff_element['content'], 'y': diff_element_normal['content']})

    result.sort(key=lambda x:x['x'])

    diff_model = diff_markov_chains(model, model)
    diff_model_normal = diff_markov_chains(model_norm, model_norm)
    diff_model_n_non_normal = diff_markov_chains(model, model_norm)

    print 'non normal model %s ' % diff_model['content']
    for result_el in result:
        print result_el

    #    model.visualise(100)
    model_diffs = [
            {'x': diff_model_normal['content'], 'y': diff_model_n_non_normal['content']},
            {'x': diff_model['content'], 'y': diff_model_n_non_normal['content']}
    ]
    vis.visualise(result, x_title='diff non normal', y_title='diff normal', spec_symbols=model_diffs)


if __name__ == '__main__':
    log.info('extract messages')
    result = extract_messages("c:/temp/tweets2009-12.txt",limit=0)
    log.info('creating users set')
    users = set(tools.flush(result, by_what=lambda x:x['user']))

    model_main = markov_chain('main', booster)
    result = []
    log.info('---------users to find is %s-------------------------------' % len(users))
    loaded_users = []
    for user in users:
        log.info('load user %s' % user)
        loaded_user = engine.scrap(user, neighbourhood=0)
        if not loaded_user:
            continue
            
        model_main = create_model(loaded_user, mc=model_main)
        create_model(loaded_user)
        loaded_users.append(loaded_user)

    log.info('---------start process differences of models--------------')
    for user in loaded_users:
        model_current = markov_chain.create(user.name_,booster)
        diff_element = diff_markov_chains(model_main, model_current)
        result.append({'name': user.name_, 'x': diff_element['content'], 'y': user.timeline_count})
        log.info('create difference... %s' % diff_element['content'])

    diff_main = diff_markov_chains(model_main, model_main)
    nodes, edges = model_main.get_unique_nodes_edges()
    model_diffs = [
            {'x': diff_main['content'], 'y': float(edges) / nodes},
    ]
    vis.visualise(result,
                  header='diff and tweets count',
                  x_title='difference between this and main',
                  y_title='count tweets',
                  spec_symbols=model_diffs)

    model_main.visualise(100)



##visualise





