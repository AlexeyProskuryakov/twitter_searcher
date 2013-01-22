from model.db import db_handler
from search_engine.twitter_engine import tweepy_engine
import tools
__author__ = '4ikist'

def load_users_by_star_friend(star_name):
    engine = tweepy_engine(out=db_handler(host_='localhost', port_=27027, db_name_='ttr_test'))
    engine.get_relations_of_user(star_name)


def get_user_timeline(user_name):
    out = db_handler(host_='localhost', port_=27017, db_name_='ttr_exp')
    engine = tweepy_engine(out=out)
    user = engine.get_user_info(user_name)
    user._id = user.name_
    out.save_user(user.serialise())
    return user

def get_user(user_name):
    db = db_handler(host_='localhost', port_=27017, db_name_='ttr_tl')
    user = db.get_user({'name_':tools.imply_dog(user_name,with_dog=True)})
    return user

if __name__ == '__main__':
    get_user_timeline('GazetaRu')
#    import text_proc.text_processing as tp
#    import analysing_data.markov_chain_machine as mc_m
#    from analysing_data.booster import db_mc_handler
#    from visualise.vis_networkx import draw_graph
#    booster = db_mc_handler(truncate=True)
#
#    user = get_user('navalny')
#    timeline = tools.flush(user.timeline,by_what=lambda x:tp.get_words(x['text'],is_normalise=True))[:10]
#    mc = mc_m.create_model(timeline,'navalny',booster)
#    #mc = mc_m.markov_chain('navalny',booster)
#    draw_graph(mc)
#
