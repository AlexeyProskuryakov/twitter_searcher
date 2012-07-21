#-*- coding: utf-8 -*-
import webbrowser

import  tweepy
import loggers
from model.db import db_handler

from model.functions import get_statistic_of
from model.tw_model import user
from model.diff_machine import difference

__author__ = 'Alesha'

log = loggers.logger

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
#todo   create heirarhy of this class engine and web driver engine, maybe use some SOA? searcher - filler|separator|manager - database


def init_account():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    verifier = raw_input('PIN: ').strip()
    auth.get_access_token(verifier)
    log.info( 'key: %s'% auth.access_token.key)
    log.info( 'secret: %s'% auth.access_token.secret)
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
        log.debug('getting user info for user: %s'%m_user.screen_name)
        result = user(m_user.screen_name)
        try:
            followers = m_user.followers()
            friends = m_user.friends()
            lists = m_user.lists()
            result.followers_count = len(followers)
            result.friends_count = len(friends)
            result.list_count = len(lists)
            #todo it must be in some another method and may be class, not? -,
            timeline = [element.text for element in m_user.timeline()] #retieving user perls
            result.tweets_stat = get_statistic_of(timeline) #creating statistic of user perls
            #todo............................................................
            result.timeline = timeline

            result.tweets_count = len(timeline)
            result.friends = self.flush(friends)
            result.followers = self.flush(followers)
            result.lists = self.flush(lists, lambda x:x.name)

            return {'result': result, 'followers': followers, "friends": friends, 'lists': lists}
        except Exception as e:
            log.exception( e)
            log.warn('no info for user...')
        return None

    #todo throw out this method from here
    def get_user_diff(self, user):
        tw_user = self.get_user_by_name(user.name)
        my_user = self.db.get_user_by_name()
        diff = difference(my_user, tw_user)
        return diff


    def __prepear_user_info(self,start_user):
        """
        preparing user info for scrapping
        return object which return .get_user_info or None
        """
        if type(start_user) in (type(str()),type(unicode())):
            start_user = self.get_user_by_name(start_user)

        #if start user is None - getting from db
        if not start_user:
            log.debug('start user is null, loading from db not searched')
            start_user = self.db.get_not_searched_name()
            if start_user:
                start_user = self.get_user_by_name(start_user)
            else:
                return

        user_obj = self.get_user_info(start_user)
        return user_obj

    def scrap(self, start_user, by_what='followers', by_what_left='friends'):
        """
        input: start_user - is tweepy user obj or simple name
        by_what - is parameter of create_user func. [followers,friends]
        """
        start_user_obj = self.__prepear_user_info(start_user)
        if not start_user_obj:
            return
        start_user_name = start_user_obj['result'].name

        rel_users = []

        #prepearing input objects users, by the use of input params 'by_what' and user_obj (info about user in interested model and some additional data)
        rel_users_in = [{'user':user,'relation':by_what} for user in start_user_obj[by_what] if by_what]
        rel_users_in.extend([{'user':user,'relation':by_what} for user in start_user_obj[by_what_left] if by_what_left])

        for user_related in rel_users_in:
            #user in tweepy model, from followers or friends which are part of start user
            t_user_related = user_related['user']
            relation = user_related['relation']
            log.debug('for user %s <--- related by --- %s ---> %s (another user)'%(start_user_name, relation, t_user_related.screen_name))
            #forming interested user model
            rel_user_obj = self.get_user_info(t_user_related)
            rel_users.append(t_user_related)
            if not rel_user_obj:
                continue
            self.db.save_user(rel_user_obj['result'].serialise())


        for user in rel_users:
            log.debug('scrapping %s which is sibling for user %s'%(user.screen_name,start_user_name))
            self.scrap(user)

        del rel_users


engine = engine(inited=True)
engine.scrap(engine.api.me())
