from analysing_data import mc_difference_logic
from analysing_data.booster import db_booster
from analysing_data.markov_chain_machine import markov_chain
import loggers
from model.db import db_handler
from properties import props
from search_engine.engines import tweepy_engine
import tools
from visualise import vis_machine


__author__ = '4ikist'

db_handler = db_handler(truncate=False)
api_engine = tweepy_engine(db_handler=db_handler)

db = api_engine.db

booster = db_booster(truncate=False)
vis_processor = vis_machine

log = loggers.logger


def process_names(file_name, class_name):
    """
    get from file ser names, scrapping saving and forming markov chains for any user timeline
    """
    names = open(file_name).readlines()
    for name in names:
        log.info("start processing name %s" % name)

        api_engine.scrap(tools.imply_dog(name))
        db.set_class(name, class_name)
        user = db.get_user({'name_': name})
        mc = markov_chain(user, booster)
        messages = [el['text'] for el in user.timeline]
        for message in messages:
            mc.add_message(message)
        mc.save()
    return names


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
    n = len(models)
    prev_model_id_ = booster.sum_models(models[0].model_id_, models[1].model_id_)
    for i in range(2, n):
        prev_model_id_ = booster.sum_models(prev_model_id_, models[i].model_id_)
    return markov_chain.create(prev_model_id_, booster)


if __name__ == '__main__':
    names = process_names('input_names', 'spam')
    models = get_models(names)
    big_model = create_one_big_model(models)
    log.info("big model: %s" % big_model.model_id_)
    big_model.visualise()