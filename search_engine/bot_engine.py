#-*- coding: utf-8 -*-
import webbrowser
import time

import  tweepy
import loggers
from model.db import db_handler

from model.functions import get_statistic_of_tweets, get_mention_weight,_hash_tag_
from model.tw_model import user
from model.diff_machine import difference
from properties import props

__author__ = 'Alesha'

log = loggers.logger

CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

max_time_line = 20


#todo create stateless

#todo   create heirarhy of this class engine and web driver engine, maybe use some SOA?
#todo   searcher - filler|separator|manager - database


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

    def __flush(self, data, by_what=lambda x:x.screen_name):
        """
        returning list of parameters which retrieving used lambda name
        """
        return [by_what(element) for element in data]

    def __get_by_name(self,from_,what, by_what=lambda x:x.screen_name):
        users = [e for e in from_ if what == by_what(e)]
        if len(users):
            return users[0]
        return None

    def __prepare_user_t_object(self,start_user):
        """
        preparing user info for scrapping
        return object of user in
        """
        if type(start_user) in (type(str()),type(unicode())):
            return self.get_user_by_name(start_user)

        if isinstance(start_user,tweepy.User):
            return start_user

        #if start user is None - getting from db
        if not start_user:
            log.debug('start user is null, loading from db not searched')
            start_user = self.db.get_not_searched_name()
            if start_user:
                start_user = self.get_user_by_name(start_user)
            else:
                return None
            return start_user


    def get_user_by_name(self, user_name):
        """
        returning user in tweepy model with user_name name
        """
        if str(user_name)[0]!='@':
            user_name = '@'+user_name
        try:
            t_user = self.api.get_user(user_name)
            return t_user
        except Exception as e:
            log.warn('in getting user by name exceptions is: %s'%e)
            raise e




    def _get_relations(self,t_user,statistic_of_text):
        """
        return friends, followers, names which this user mention
        in db it will be:
        object: {followers: [names], friends:[names], mentions:[{}]}
        subject: also in tweepy model, {followers:[users], ...}
        """
        followers = t_user.followers()
        friends = t_user.friends()

        mentions = [{'entity':obj['entity'],'weight':get_mention_weight(obj)} for obj in statistic_of_text if obj['type'] == _hash_tag_  and obj['entity'][0]== '@']
        mentions_names = self.__flush(mentions,lambda x:x['entity'])
        mentions_users = []
        users = followers
        users.extend(friends)
        
        for mention_name in mentions_names:
            t_user_related = self.__get_by_name(users,mention_name)
            if t_user_related:
                mentions_users.append(t_user_related)
            elif mention_name == t_user.screen_name:
                continue
            else:
                mt_user = self.get_user_by_name(mention_name)
                if mt_user:
                    mentions_users.append(mt_user)

        return {
            'object':{'followers':self.__flush(followers), 'friends':self.__flush(friends),'mentions':mentions},
            'subject':{'followers':followers,'friends':friends, 'mentions':mentions_users }
        }

    def _get_data(self,t_user):
        """
        forming user in our model to save into db
        """
        result = user(t_user.screen_name)
        result.real_name = t_user.name
        lists = t_user.lists()
        result.list_count = len(lists)
        result.lists = self.__flush(lists, lambda x:x.name)

        result.followers_count = t_user.followers_count
        result.friends_count = t_user.friends_count

        if t_user.protected:
            log.debug('user %s is protected... skip him'%t_user.screen_name)
            return None
        timeline = [{'text':element.text,'retweets':element.retweet_count,'initted':element.created_at.strftime(props.time_format)} for element in t_user.timeline()] #retieving user perls
        result.timeline = timeline

        result.timeline_count = t_user.statuses_count
        result.initted_ = t_user.created_at.strftime(props.time_format)

        return result



    def get_user_info(self, t_user):
        """
        input is user tweepy object
        evaluating statistic of tweets timeline (perls, text, hashtags, etc)
        return result: user obj in my model, followers: list of tweepy model users, friends: like followers
        """
        log.debug('getting user info for user: %s'%t_user.screen_name)
        try:
            #forming user data
            user = self._get_data(t_user)
            #forming statistic of tweets
            if not user:
                return None
            user.tweets_stat = get_statistic_of_tweets(self.__flush(user.timeline,lambda x:x['text'])) #creating statistic of user perls
            #retrieving relations, on statistic too

            relation_object = self._get_relations(t_user,user.tweets_stat)
            user.set_relations(relation_object['object'])

            return {'object': user, 'subject': relation_object['subject'] }
        except Exception as e:
            log.exception( e)
            log.warn('error in info for user...\n%s'%'\n'.join(t_user.__dict__))
            raise e



    def get_user_diff(self, user):
        tw_user = self.get_user_by_name(user.name)
        my_user = self.db.get_user_by_name()
        diff = difference(my_user, tw_user)
        return diff




    def scrap(self, start_user, neighbourhood=1, level =0):
        """
        Retrieving users from twitter and reflect to our model.
        Берем птичку, берем ее окрестность. Идем в следующую птичку рядом с этой окрестностью. Сверяясь с буфером уже найденных.
        
        input: start_user - is tweepy user obj or simple name
        by_what - is parameter of create_user func. [followers,friends]
        """
        try:

            start_user_obj = self.__prepare_user_t_object(start_user)
            if not start_user_obj:
                return

            log.debug('scrapping user: %s, at neigh: %s in level: %s'%(start_user_obj.screen_name,neighbourhood,level))
            user_info = self.get_user_info(start_user_obj)
            if not user_info:
                return
            #saving interested user
            self.db.save_user(user_info['object'].serialise())

            related_users = []
            if neighbourhood >= level:
                neighbourhood_users = []
                neighbourhood_users.extend(user_info['subject']['followers'])
                neighbourhood_users.extend(user_info['subject']['friends'])
                neighbourhood_users.extend(user_info['subject']['mentions'])
                neighbourhood_users = set(neighbourhood_users)

                for n_user in neighbourhood_users:
                    related_users.append(n_user)
                    related = self.scrap(n_user,neighbourhood=neighbourhood,level=level+1)
                    if related:
                        related_users.extend(related)

                related_users = set(related_users).difference(neighbourhood_users)
            return related_users

        except Exception as e:
            log.warn('in scrapping exception as %s'%e)


if __name__ == '__main__':
    engine = engine(inited=True)
    engine.scrap('@linoleum2k12',neighbourhood=2)


