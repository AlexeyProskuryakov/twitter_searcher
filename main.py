from properties import props
from search_engine.tweepy_engine import engine

__author__ = '4ikist'
if __name__ == '__main__':

    api_engine = engine()
    if not props.is_debug:
        name = raw_input('Type name of start: (it must use be with @ at prefix)').strip()
    else:
        name = '@linoleum2k12'
    api_engine.scrap(name)