from analysing_data import markov_chain_machine
from analysing_data.markov_chain_machine import markov_chain
import text_proc.text_processing as tp
from analysing_data.booster import db_mc_handler
from model.db import db_handler
from search_engine.twitter_engine import tweepy_engine
from analysing_data.mc_difference_logic import diff_markov_chains
import tools

__author__ = '4ikist'

db = db_handler(host_='localhost', port_=27017, db_name_='ttr_exp')
boost = db_mc_handler()
engine = tweepy_engine(out=db)


def get_users_data(user_name1, user_name2):
    user1 = engine.get_user_info(user_name1)
    user2 = engine.get_user_info(user_name2)

    db.save_user(user1.serialise())
    db.save_user(user2.serialise())

    timeline1 = tools.flush(user1.timeline, by_what=lambda x: tp.get_words(x['text'], is_normalise=True))[:10]
    timeline2 = tools.flush(user2.timeline, by_what=lambda x: tp.get_words(x['text'], is_normalise=True))[:10]
    print len(timeline1)
    print len(timeline2)
    mc1 = markov_chain_machine.create_model(timeline1, user_name1, boost)
    mc2 = markov_chain_machine.create_model(timeline2, user_name2, boost)

    return mc1, mc2


def form_timeline(user_timeline):
    true_timeline = tools.flush(user_timeline, by_what=lambda x: tp.get_words(x['text'], is_normalise=True))
    return true_timeline

if __name__ == '__main__':
#    models = get_users_data('navalny', 'MedvedevRussia')
#    print diff_markov_chains(models[0], models[1])
#    engine.get_relations_of_user('navalny')

#    user = engine.get_user_info('GoogleRussia')
#    db.save_user(user.serialise())
#    user = db.get_user({'name_':'@GoogleRussia'})
#
#    print len(user.timeline)
#    print user.timeline_count

    user = db.get_user({'name_': '@GoogleRussia'})
    time_line = form_timeline(user.timeline)
    mc = markov_chain_machine.create_model(time_line,user.name_,boost)
    mc.print_me()
    diff_markov_chains(mc,mc)