from model.db import db_handler
from properties import props
from search_engine.engines import tweepy_engine

__author__ = '4ikist'

def extract_users():
    db = db_handler()


if __name__ == '__main__':

    api_engine = tweepy_engine()
    if not props.is_debug:
        name = raw_input('Type name of start: (it must use be with @ at prefix)').strip()
    else:
        name = '@linoleum2k12'
    api_engine.scrap(name)