#-*- coding: utf-8 -*-
import webbrowser
import  tweepy
from tweepy.models import User

__author__ = 'Alesha'

CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

max_time_line = 20

def init_account():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    verifier = raw_input('PIN: ').strip()
    auth.get_access_token(verifier)
    print 'key: ', auth.access_token.key
    print 'secret: ', auth.access_token.secret
    return auth.access_token.key, auth.access_token.secret


class bot:
    def __init__(self, inited=False):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        if inited:
            self.access_token, self.access_token_secret = init_account()
            self.auth.set_access_token(self.access_token, self.access_token_secret)
        else:
            self.auth.set_access_token(access_token, access_token_secret)

        self.__init_api()

    def __init_api(self):
        self.api = tweepy.API(self.auth)
        self.folowers = [{'name': user.screen_name, 'obj': user} for user in tweepy.Cursor(self.api.followers).items()]
        self.friends = [{'name': user.screen_name, 'obj': user} for user in tweepy.Cursor(self.api.friends).items()]
        self.timeline = [{'text': status.text, 'obj': status} for status in tweepy.Cursor(self.api.home_timeline).items(
            max_time_line)]

    def map_reduce(self, what, map=lambda what:what['obj'].friends(),
                   reduce=lambda user:{'name': user.screen_name, 'obj': user}):
        """
        FUUUUUUUUUUUCK!
        """
        return [reduce(user) for user in map(what)]

    def get_friends_of_user(self, user):
        self.map_reduce(user)

    def get_statuses_text_of_user_name(self, user):
        string_result = ''
        timeline = self.map_reduce(
                {'name': 'input',
                 'obj': self.api.get_user(user)},
                                                map=lambda what:what['obj'].timeline(),
                                                reduce=lambda input:{'text': input.text, 'obj': input})
        print timeline#todo
        return string_result

bot = bot()
#print bot.folowers
#print bot.friends
#print bot.timeline
#print bot.map_reduce(bot.folowers[0])
print bot.get_statuses_text_of_user_name('twitter')