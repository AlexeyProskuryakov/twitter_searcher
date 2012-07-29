#-*- coding: utf-8 -*-
import webbrowser
import time
import  tweepy
import loggers
from model.diff_machine import create_difference

from model.db import db_handler
from model.functions import get_mention_weight,_hash_tag_,create_statistic_of_tweets
from model.tw_model import *
from properties import props
from properties.props import CONSUMER_SECRET, CONSUMER_KEY
import tools

__author__ = 'Alesha'

log = loggers.logger





#todo   create heirarhy of this class engine and web driver engine, maybe use some SOA?
#todo   searcher - filler|separator|manager - database

class engine(object):
    def init_engine(self):
        pass
    def get_user_info(self,user,with_relations=False):
        pass
    def scrap(self,start_user, neighbourhood=props.def_n, level =0):
        pass


class tweepy_engine(engine):
    def init_account(self):
        """
        init account used for retrieving access req
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        webbrowser.open(auth_url)
        verifier = raw_input('PIN: ').strip()
        auth.get_access_token(verifier)
        log.info( 'access_token: %s'% auth.access_token.key)
        log.info( 'access_token_secret: %s'% auth.access_token.secret)
        log.info("!!! save it into properties at next time or now !!!")
        return auth.access_token.key, auth.access_token.secret

    def __init__(self, inited=props.is_inited(), db_handler=db_handler()):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        if not inited:
            self.access_token, self.access_token_secret = self.init_account()
            self.auth.set_access_token(self.access_token, self.access_token_secret)
        else:
            self.auth.set_access_token(props.access_token, props.access_token_secret)

        self.api = tweepy.API(self.auth)
        self._count_requests = int(1)
        log.debug("auth +1")
        self.db = db_handler

   
    def _prepare_user_t_object(self,start_user):
        """
        preparing user info for scrapping
        return object of user in tweepy model
        """
        if type(start_user) in (type(str()),type(unicode())):
            if self.db.verify_user(start_user).status == m_user_status.s_none:
                return self._get_user_by_name(start_user)
            else:
                log.warn('this user is saved')

        if isinstance(start_user,tweepy.User):
            if self.db.verify_user('@'+start_user.screen_name).status == m_user_status.s_none:
                return start_user
            else:
                log.warn('this user is saved')

        #if start user is None - getting from db
        if not start_user:
            log.debug('start user is null, loading from db not searched')
            start_user = self.db.get_not_searched_name()
            if start_user:
                start_user = self._get_user_by_name(start_user)
            else:
                return None
            return start_user


    def _get_user_by_name(self, user_name):
        """
        returning user in tweepy model with user_name name
        """
        if str(user_name)[0]!='@':
            user_name = '@'+user_name
        try:
            t_user = self.api.get_user(user_name)
            self._count_requests+=1
            log.debug("get user +1")
            return t_user
        except Exception as e:
            log.warn('in getting user by name exceptions is: %s \n with username: %s'%(e,user_name))
            raise e



    def _get_user_relations(self,t_user,statistic_of_text):
        followers = t_user.followers()
        friends = t_user.friends()
        self._count_requests+=2
        log.debug("get followers and friends +2")
        mentions = [m_hash_dict({'entity':obj['entity'],'weight':get_mention_weight(obj)}) for obj in statistic_of_text if obj['type'] == _hash_tag_  and obj['entity'][0]== '@']
        return {'object':{'followers':tools.flush(followers), 'friends':tools.flush(friends),'mentions':mentions},
                'additional':{'followers':followers,'friends':friends, 'mentions':mentions}}

    def _get_related(self,additional):
        """
        get all t_users which have any relation
        """
        followers = additional['followers']
        friends = additional['friends']
        mentions = additional['mentions']

        mentions_names = tools.flush(mentions,lambda x:x['entity'])
        mentions_users = []
        users = followers
        users.extend(friends)
        
        for mention_name in mentions_names:
            #find in followers and friends user with name from mentions
            t_user_related = tools.get_by_name(users,mention_name)
            if t_user_related:
                #if founded
                mentions_users.append(t_user_related)
            #else, retrieving this user by mention_name
            else:
                try:
                    t_user = self._get_user_by_name(mention_name)
                    if t_user:
                        mentions_users.append(t_user)
                except Exception:
                    log.warn('exception in load user %s'%mention_name)
                    continue

        return {'followers':followers,'friends':friends, 'mentions':mentions_users}


    def _get_data(self,t_user):
        """
        forming user in our model to save into db
        """
        result = m_user('@'+t_user.screen_name)
        result.real_name = t_user.name
        lists = t_user.lists()
        self._count_requests+=1
        log.debug("get lists +1")
        result.list_count = len(lists)
        result.lists = tools.flush(lists, lambda x:x.name)
        
        result.followers_count = t_user.followers_count
        result.friends_count = t_user.friends_count
        if t_user.protected:
            log.debug('user %s is protected... skip him'%t_user.screen_name)
            return None
        t_timeline = t_user.timeline()

        self._count_requests+=1
        log.debug("get timeline +1")

        timeline = [m_hash_dict({'text':element.text,'retweets':element.retweet_count,'initted':element.created_at}) for element in t_timeline] #retieving user perls
        result.timeline = timeline

        result.timeline_count = t_user.statuses_count
        result.inited_ = t_user.created_at.strftime(props.time_format)

        return result



    def get_user_info(self, start_user, with_relations = True):
        """
        input is user tweepy object
        evaluating statistic of tweets timeline (perls, text, hashtags, etc)
        return result: user obj in my model, followers: list of tweepy model users, friends: like followers
        """


        t_user = None
        try:
            start_user_obj = self._prepare_user_t_object(start_user)
            if not start_user_obj:
                  return
            t_user = start_user_obj
            log.debug('getting user info for user: %s'%'@'+t_user.screen_name)
            #forming user data
            user = self._get_data(t_user)
            #forming statistic of tweets
            if not user:
                return None
            user.tweets_stat = create_statistic_of_tweets(user) #creating statistic of user perls
            #retrieving relations, on statistic too

            relation_object = self._get_user_relations(t_user,user.tweets_stat)
            user.set_relations(relation_object['object'])
            if with_relations:
                relations = self._get_related(relation_object['additional'])
                return {'object': user, 'relations': relations}
            else:
                return user
        except Exception as e:
            log.exception(e)
            log.info("counts of request is: %s"%self._count_requests)
            if not t_user:
                t_user = {'name':start_user, 'some bad':'yes'}

            log.warn('error in info for user...\n%s'%'\n'+str(t_user.__dict__))
            if 'Rate limit exceeded' in str(e):
                log.info('oook wil be sleep...')
                time.sleep(3600)
            if 'Invalid / expired Token' in str(e):
                log.exception("!!!!!!!! CHANGE ACCESS TOKEN !!!!!!!!")
                raise e


    def scrap(self, start_user, neighbourhood=props.def_n, level =0):

        """
        Retrieving users from twitter and reflect to our model.
        retrieve user and some of him neighbourhood in graph model by retrieving his relations (foll,friends,mentions)
        process user used for functions.py file

        input: start_user - is tweepy user obj or simple name
        by_what - is parameter of create_user func. [followers,friends]
        """
        log.info("start scrap user: %s"%start_user)
        try:
            user_info = self.get_user_info(start_user)
            if not user_info:
                return
            user_to_save = user_info['object'].serialise()
            log.debug('scrapping user: %s\nat neigh: %s in level: %s'%(user_to_save,neighbourhood,level))
            #saving interested user
            self.db.save_user(user_to_save)

            relations_in_t_model  = user_info['relations']
            related_users = []
            if neighbourhood >= level:
                neighbourhood_users = []
                neighbourhood_users.extend(relations_in_t_model['followers'])
                neighbourhood_users.extend(relations_in_t_model['friends'])
                neighbourhood_users.extend(relations_in_t_model['mentions'])
                neighbourhood_users = set(neighbourhood_users)

                for n_user in neighbourhood_users:
                    related_users.append(n_user)
                    related = self.scrap(n_user,neighbourhood=neighbourhood,level=level+1)
                    if related:
                        related_users.extend(related)

                related_users = set(related_users).difference(neighbourhood_users)
            return related_users

        except Exception as e:
            log.exception(e)
            log.warn('in scrapping exception as %s'%e)

    def diff_process(self):
        diff_users = self.db.get_users_for_diff()
        for user in diff_users:
            try:

                log.info('processing diffs for: %s'%user)
                t_user = self._get_user_by_name(user)
                m_user_now = self.get_user_info(t_user,with_relations=False)
                m_user_prev = self.db.get_user({'name_':m_user_now.name_})

                diff = create_difference(user_before=m_user_prev,user_now=m_user_now)
                self.db.save_diffs(diff.serialise())

            except Exception as e:
                log.warn('some exception in e: %s'%e)
                log.exception(e)
                if 'Rate limit exceeded' in str(e):
                    log.info('oook wil be sleep...')
                    time.sleep(3600)



if __name__ == '__main__':
    engine_ = tweepy_engine()
    engine_.diff_process()
    





