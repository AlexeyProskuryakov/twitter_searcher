#-*- coding: utf-8 -*-
import webbrowser

import  tweepy
from model.db import db_handler

from model.functions import get_statistic_of
from model.tw_model import user

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


class engine:
    def __init__(self, inited=False, db_handler=db_handler()):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        if not inited:
            self.access_token, self.access_token_secret = init_account()
            self.auth.set_access_token(self.access_token, self.access_token_secret)
        else:
            self.auth.set_access_token(access_token, access_token_secret)

        self.__init_api()
        self.db = db_handler

    def __init_api(self):
        self.api = tweepy.API(self.auth)

    #        self.folowers = [{'name': user.screen_name, 'obj': user} for user in tweepy.Cursor(self.api.followers).items()]
    #        self.friends = [{'name': user.screen_name, 'obj': user} for user in tweepy.Cursor(self.api.friends).items()]
    #        self.timeline = [{'text': status.text, 'obj': status} for status in tweepy.Cursor(self.api.home_timeline).items(
    #            max_time_line)]

    def flush(self, data, name=lambda x:x.screen_name):
        return [name(element) for element in data]

    def get_user_by_name(self, user_name):
        return self.api.get_user(user_name)

    def create_user(self, m_user):
        """
        input is user tweepy object
        return result: user obj in my model, followers - list of tweepy model users, friends - also
        """

        result = user(m_user.screen_name)
        try:
            followers = m_user.followers()
            friends = m_user.friends()
            lists = m_user.lists()
            result.followers_count = len(followers)
            result.friends_count = len(friends)
            result.list_count = len(lists)
            timeline = [element.text for element in m_user.timeline()]
            result.tweets_stat = get_statistic_of(timeline)
            result.tweets_count = len(timeline)
            result.friends = self.flush(friends)
            result.followers = self.flush(followers)
            result.lists = self.flush(lists, lambda x:x.name)
            return {'result': result, 'followers': followers, "friends": friends, 'lists': lists}
        except Exception as e:
            print e
        return None

    def scrap(self, start_user, by_what='followers'):
        """
        input: start_user - is tweepy user obj
        by_what - is parameter of create_user func.
        """

        user_obj = self.create_user(start_user)
        if not user_obj:
            return
            #prepearing list of temp users
        rel_users = []
        #for followers or friends...
        for user_related in user_obj[by_what]:
            print 'related', user_related.screen_name
            #flushing user in my model
            rel_user_obj = self.create_user(user_related)
            if not rel_user_obj:
                continue
            self.db.save_user(rel_user_obj['result'].serialise())
        for user in rel_users:
            print user.screen_name
            self.scrap(user)
        del rel_users


engine = engine(inited=True)
engine.scrap(engine.api.me())
