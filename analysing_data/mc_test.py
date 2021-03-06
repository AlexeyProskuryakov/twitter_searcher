from analysing_data.booster import db_mc_handler
from analysing_data.markov_chain_machine import *
from analysing_data.mc_difference_logic import diff_markov_chains
from db_scripts import twitter_timeline_parser
from loggers import logger

__author__ = '4ikist'

__doc__ = """
Create user : model mapping/

Test hi load

Create and test clustering.
For some user. For some theme.

"""

log = logger

def test_difference_logic(markov_chain_l, markov_chain_r):
    difference_element = diff_markov_chains(markov_chain_l, markov_chain_r)
    log.info('difference element is: %s' % difference_element)

def split_to_words(message):
    return str(message).split()

def test_generate_model():
    messages = twitter_timeline_parser.extract_messages("c:/temp/tweets2009-12.txt", limit=100)
    log.info('\n'.join([message['words'] for message in messages]))
    log.info(len(messages))
    booster = db_mc_handler()
    mc_l = markov_chain('test',booster)
    for i  in range(len(messages)):
        message = messages[i]
        mc_l.add_message(split_to_words(message['words']))
        log.info('appending %s words: %s relations: %s' % (i, mc_l.words_count_, mc_l.relations_count_))

    log.info('................................')



def test_model_():
    booster = db_mc_handler(truncate=True)

    mc1 = markov_chain('left_test', booster,n_of_gram_=2)
    mc2 = markov_chain('right_test', booster,n_of_gram_=2)

    mc1.add_message(['a', 'b', 'c', 'd'])
    mc1.add_message(['a', 'b', 'c', 'd'])
    mc1.add_message(['a1', 'b1', 'c1', 'd1'])
    mc1.add_message(['a','a1','b','b1','c','c1','d','d1'])

    mc2.add_message(['a', 'b', 'c', 'd'])
    mc2.add_message(['a2', 'b2', 'c2', 'd2'])

    mc1.save()
    mc2.save()

    mc1.print_me()
    mc2.print_me()

#    mc1.visualise(8)
#    mc2.visualise(8)


if __name__ == '__main__':
    test_model_()


    

