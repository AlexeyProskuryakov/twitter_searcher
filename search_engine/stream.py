import tweepy
from search_engine import tweepy_engine
__author__ = 'Alesha'
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status


bot = tweepy_engine()