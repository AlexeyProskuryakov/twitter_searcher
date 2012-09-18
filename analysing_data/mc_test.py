from analysing_data.booster import db_booster
from analysing_data.markov_chain_machine import markov_chain
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
    mc = markov_chain(model_id_='test',)
    for message in messages:
        mc.append(message)
    booster = db_booster()
    mc.boost(booster)
    return mc

def test_logic(markov_chain):
    pass
def main():
    pass


if __name__ == '__main__':
    mc = markov_chain(['a', 'b', 'a', 'c'])
    mc.append(['a', 'b', 'c', 'd'])

    markov_chain._print(mc,log.info)

    mc1 = markov_chain(['c', 'd', 'c', 'e'])
    mc1.append(['a', 'b', 'c', 'd'])

    markov_chain._print(mc1,log.info)

    mc.extend(mc1)
    print 'extend:'
    markov_chain._print._print(mc,log.info)

    print mc.get_all_relations('a')
#    mc.append(['a','b','c'])
#    mc = markov_chain(['a','b','c','a','b','b','c'],3)
