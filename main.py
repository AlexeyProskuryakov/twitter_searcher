from analysing_data import mc_difference_logic
from analysing_data.booster import db_mc_handler
from analysing_data.markov_chain_machine import markov_chain
import loggers
from model.db import db_handler
from properties import props
from search_engine.engines import tweepy_engine
import tools
from visualise import vis_machine


__author__ = '4ikist'

db_handler = db_handler(truncate=False)

api_engine = tweepy_engine(out=db_handler)

booster = db_mc_handler(truncate=False)
vis_processor = vis_machine

log = loggers.logger

def model_splitter(message):
    message_ = message.split()
    return message_


def process_names(file_name, class_name):
    """
    get from file ser names, scrapping saving and forming markov chains for any user timeline
    """
    names = open(file_name).readlines()
    result = []
    for name in names:
        name = tools.imply_dog(name, with_dog=True).strip()
        log.info("start processing name %s" % name)

        user = api_engine.scrap(name)
        db_handler.set_class(name, class_name)
        mc = markov_chain(name, booster)

        messages = []
        for t_el in user.timeline:
            log.debug('>>>>%s' % t_el)
            if t_el:
                mc.add_message(model_splitter(t_el['text']))

        mc.save()
        result.append(mc)
    return result


def get_models(model_ids):
    result = []
    for model_id in model_ids:
        result.append(markov_chain.create(model_id, booster))
    return result


def process_models(models):
    result = []
    for model in models:
        for model_ in models:
            if model != model_:
                result.append(mc_difference_logic.diff_markov_chains(model, model_))
    log.info(sum([el['content'] for el in result]))
    return result


def create_one_big_model(models):
    log.info('create big model')
    n = len(models)
    prev_model_id_ = booster.sum_models(models[0].model_id_, models[1].model_id_)
    for i in range(2, n):
        log.info('difference between: %s  < -- > %s' % (prev_model_id_, models[i].model_id_))
        prev_model_id_ = booster.sum_models(prev_model_id_, models[i].model_id_)
        log.info('is win! : ' + prev_model_id_)
    return markov_chain.create(prev_model_id_, booster)


if __name__ == '__main__':
#    models = process_names('spam_names', 'spam')
#    big_model = create_one_big_model(models)
    big_model = markov_chain.create('@alemapimeon',booster)
#    log.info("big model: %s" % big_model.model_id_)
    big_model.visualise(100)