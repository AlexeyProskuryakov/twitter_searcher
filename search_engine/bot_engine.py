#-*- coding: utf-8 -*-
import webbrowser

import  tweepy
from model.db import db_handler

from model.functions import get_statistic_of
from model.tw_model import user
from model.diff_machine import difference

__author__ = 'Alesha'

CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

max_time_line = 20

#todo   you must know about users: if two requests will be evaluate in not far difference time, what changed?
#todo   may be some followers will add or friends or another difference will be
#todo   get counts of followers\friends\lists
#todo   get counts of twitter accounts in social nets.
#todo   what about times in your program?
#todo   create heirarhy of this class engine and web driver engine


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

        self.api = tweepy.API(self.auth)
        self.db = db_handler

    def flush(self, data, name=lambda x:x.screen_name):
        """
        returning list of parameters which retrieving used lambda name
        """
        return [name(element) for element in data]

    def get_user_by_name(self, user_name):
        """
        returning user in tweepy model with user_name name
        """
        return self.api.get_user(user_name)

    def get_user_info(self, m_user):
        """
        input is user tweepy object
        evaluating statistic of tweets timeline (perls, text, hashtags, etc)
        return result: user obj in my model, wollowers: list of tweepy model users, friends: like followers
        """
        result = user(m_user.screen_name)
        try:
            followers = m_user.followers()
            friends = m_user.friends()
            lists = m_user.lists()
            result.followers_count = len(followers)
            result.friends_count = len(friends)
            result.list_count = len(lists)
            #todo it must be in some another method and may be class, not?
            timeline = [element.text for element in m_user.timeline()] #retieving user perls
            result.tweets_stat = get_statistic_of(timeline) #creating statistic of user perls
            result.timeline = timeline

            result.tweets_count = len(timeline)
            result.friends = self.flush(friends)
            result.followers = self.flush(followers)
            result.lists = self.flush(lists, lambda x:x.name)
            return {'result': result, 'followers': followers, "friends": friends, 'lists': lists}
        except Exception as e:
            print e
        return None

    def get_user_diff(self, user):
        tw_user = self.get_user_by_name(user.name)
        my_user = self.db.get_user_by_name()
        diff = difference(my_user, tw_user)
        return diff
        #here difference after tests....

    def scrap(self, start_user, by_what='followers'):
        """
        input: start_user - is tweepy user obj
        by_what - is parameter of create_user func.
        """
        if not start_user:
            start_user = self.db.get_not_searched_name()
            start_user = self.get_user_by_name(start_user)

        user_obj = self.get_user_info(start_user)
        if not user_obj:
            return

        rel_users = []
        #for followers or friends...
        for user_related in user_obj[by_what]:
            print 'related', user_related.screen_name
            #forming user in my model
            rel_user_obj = self.get_user_info(user_related)
            if not rel_user_obj:
                continue
            self.db.save_user(rel_user_obj['result'].serialise())
        for user in rel_users:
            print user.screen_name
            self.scrap(user)
        del rel_users


engine = engine(inited=True)
engine.scrap(engine.api.me())
