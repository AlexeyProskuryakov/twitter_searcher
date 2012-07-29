import tweepy
from search_engine import engines
__author__ = 'Alesha'
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status


bot = engines()