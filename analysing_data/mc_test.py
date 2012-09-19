from analysing_data.booster import db_booster
from analysing_data.markov_chain_machine import *
from analysing_data.mc_difference_logic import diff_markov_chains
from loggers import logger

__author__ = '4ikist'

__doc__ = """
Create user : model mapping/

Test hi load

Create and test clustering.
For some user. For some theme.

"""

log = logger

def test_mc(messages):
    mc = markov_chain(model_id_='test', )
    for message in messages:
        mc.append(message)
    booster = db_booster()
    mc.boost_and_save(booster)
    return mc


def test_logic(markov_chain):
    pass


def main():
    pass


if __name__ == '__main__':
    booster = db_booster(truncate=True)

    mc_l = markov_chain(['a1', 'b1', 'c1'], model_id_='left', db_booster=db_booster())
    mc_l.append(['a2', 'b1', 'c1'])
    mc_l.append(['a2', 'c1', 'a2', 'd1'])
    mc_l.append(['a2', 'd1'])

    mc_r = markov_chain(['a1', 'b1', 'c1'], model_id_='right', db_booster=db_booster())
    mc_r.append(['a3', 'b1', 'c1'])
    mc_r.append(['a3'])
    mc_r.append(['a3', 'b4', 'c3', 'd2'])
    mc_r.append(['a3', 'b4', 'c2', 'd2'])
    mc_r.append(['a3', 'b4', 'c3', 'a3'])



    markov_chain._print(mc_l, log.info)
    markov_chain._print(mc_r, log.info)

    

    mc_l.boost_and_save(db_booster())
    mc_r.boost_and_save(db_booster())

    log.info('................................')

    markov_chain._print(mc_l, log.info)
    markov_chain._print(mc_r, log.info)

    print diff_markov_chains(mc_l,mc_r)



