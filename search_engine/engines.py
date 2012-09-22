#-*- coding: utf-8 -*-
import webbrowser
import time
import  tweepy
from tweepy.error import TweepError
from differences.diff_machine import difference_factory
import loggers
from model.db import db_handler
from model.tw_model import *
from properties import props
from properties.props import CONSUMER_SECRET, CONSUMER_KEY
import tools

__author__ = 'Alesha'

log = loggers.logger

class tweepy_engine(object):
    def init_account(self):
        """
        init account used for retrieving access req
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        webbrowser.open(auth_url)
        verifier = raw_input('PIN: ').strip()
        auth.get_access_token(verifier)
        log.info('access_token: %s' % auth.access_token.key)
        log.info('access_token_secret: %s' % auth.access_token.secret)
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

        self.relations_cache = {}

    def _get_relations_cache(self, user_name):
        if self.relations_cache.has_key(user_name):
            return self.relations_cache[user_name]
        else: return None

    def _is_name_in_cache(self, user_name, r_type, name):
        if self.relations_cache.has_key(user_name):
            user_relations = self.relations_cache[user_name]
            type_relations = user_relations[r_type]
            for relation in type_relations:
                if tools.imply_dog(relation.screen_name) == tools.imply_dog(name):
                    return True
        return False


    def _get_user_by_name(self, user_name):
        """
        returning user in tweepy model with user_name name
        """
        user_name = tools.imply_dog(user_name, with_dog=True)
        try:
            t_user = self.api.get_user(user_name)
            self._count_requests += 1
            log.debug("get user +1")
            return t_user
        except Exception as e:
            log.warn('in getting user by name exceptions is: %s \n with username: %s' % (e, user_name))

            if 'Rate limit exceeded' in str(e):
                log.info('oook wil be sleep...')
                time.sleep(3600)
                return self._get_user_by_name(start_user)
            else:
                raise e

    def _get_name_from_user(self, user):
        if isinstance(user, m_user):
            return user.name_
        if isinstance(user, tweepy.User):
            return tools.imply_dog(user.screen_name, with_dog=True)
        else:
            return user

    def _get_user_relations(self, t_user):
        """
        returning object of followers and friends names with @
        also storing in cache objects in tweepy model
        """
        try:
            followers = t_user.followers()
            friends = t_user.friends()
            self.relations_cache[tools.imply_dog(t_user.screen_name, with_dog=True)] = {'followers': followers,
                                                                                        'friends': friends}
            self._count_requests += 2
            log.debug("get followers and friends +2")

            return  {'followers': [tools.imply_dog(user.screen_name, with_dog=True) for user in followers],
                     'friends': [tools.imply_dog(user.screen_name, with_dog=True) for user in friends]}

        except Exception as e:
            if 'Rate limit exceeded' in str(e):
                log.info('oook wil be sleep...')
                time.sleep(3600)
                return self._get_user_relations(t_user)

    def _prepare_user_t_object(self, start_user):
        """
        preparing user info for scrapping
        return object of user in tweepy model
        """
        if isinstance(start_user, unicode)or isinstance(start_user, str):
            try:
                t_user = self._get_user_by_name(start_user)
                return t_user
            except Exception:
                log.warn('can not load user for get him info')
                return None

        elif isinstance(start_user, tweepy.User):
            return start_user
        else:
            log.warn('can not implying user for prepare type\n %s' % start_user)

    def _get_time_line(self, t_user):
        try:
            t_timeline = t_user.timeline()

            self._count_requests += 1
            log.debug("get timeline +1")

            timeline = [
            m_hash_dict({'text': element.text, 'retweets': element.retweet_count, 'initted': element.created_at}) for
            element in t_timeline] #retieving user perls
            return timeline
        except Exception as e:
            if 'Rate limit exceeded' in str(e):
                log.info('oook wil be sleep...')
                time.sleep(3600)
                return self.get_user_info(start_user)

    def _get_data(self, t_user):
        """
        forming user in our model to save into db
        """
        result = m_user(tools.imply_dog(t_user.screen_name, with_dog=True))
        if t_user.protected:
            log.debug('user %s is protected... skip him' % t_user.screen_name)
            return None

        result.real_name = t_user.name
        lists = t_user.lists()
        self._count_requests += 1
        log.debug("get lists +1")
        result.set_lists(tools.flush(lists, lambda x:x.name), len(lists))

        result.followers_count = t_user.followers_count
        result.friends_count = t_user.friends_count

        result.favorites_count = t_user.favourites_count
        result.timeline = self._get_time_line(t_user)
        result.timeline_count = t_user.statuses_count
        result.inited_ = t_user.created_at.strftime(props.time_format)
        return result


    def get_user_info(self, start_user):
        """
        input is user tweepy object
        evaluating statistic of tweets timeline (perls, text, hashtags, etc)
        return result: user obj in my model, followers: list of tweepy model users, friends: like followers
        """
        t_user = None
        try:
            start_user_obj = self._prepare_user_t_object(start_user)
            if not start_user_obj:
                log.warn("start user is none")
                return None
            t_user = start_user_obj
            log.info('getting user info for user: %s' % '@' + t_user.screen_name)
            #forming user data
            user = self._get_data(t_user)
            if not user:
                log.warn('when getting data user is none')
                return None

            log.debug('creating statistic of user perls and hash_tags')
            #with processing by tools flushing text from timeline
            hashtags_urls_mentions = functions.get_hash_tags_urls_mentions(
                tools.flush(user.timeline, lambda x:x['text']))
            #also forming mention relations
            user.set_timeline_info(hashtags_urls_mentions)

            log.debug('retrieving relations (friends,followers)')
            relation_object = self._get_user_relations(t_user)
            user.set_relations(relation_object)

            return user

        except Exception as e:
            log.exception(e)
            log.info("counts of request is: %s" % self._count_requests)
            log.warn('error in info for user...\n%s' % '\n' + '\n'.join(t_user.__dict__.items()))

            if isinstance(e, TweepError) and 'Rate limit exceeded' in e.message:
                log.info('oook wil be sleep...')
                time.sleep(3600)
                return self.get_user_info(start_user)

            if 'Invalid / expired Token' in str(e):
                log.exception("!!!!!!!! CHANGE ACCESS TOKEN !!!!!!!!")
                raise e

    def _load_users_by_names(self, list):
        res = []
        for user in list:
            try:
                user_obj = self._get_user_by_name(tools.imply_dog(user))
                if user_obj:
                    res.append(user_obj)
            except Exception as e:
                log.warn('problems with user %s ' % user)
        return res

    def _form_relations(self, user_name, relation_types, relations_names):
        """
        input :
            name of user which form relations,
            types of relations like mentions,followers,friends,
            names of relations objects

        form relations/
        if some relation object not in cache - loading from ttr/
        if some relation type not in cache - loading from ttr/
        this method will load some user obj if it not in some relation type
        """
        log.info('start forming relations for user %s' % user_name)
        relations = self._get_relations_cache(user_name)

        for r_type in relation_types:
            if not relations.has_key(r_type):
                #getting tweepy model users which in relations
                log.info("cache have not contain this relations type [%s]" % r_type)
                relations[r_type] = self._load_users_by_names(relations_names[r_type])
                continue
            for r_name in relations_names[r_type]:
                if self._is_name_in_cache(user_name, r_type, r_name):
                    continue
                else:
                    relations[r_type].append(self._get_user_by_name(tools.imply_dog(r_name, with_dog=True)))
        return relations

    def scrap(self, start_user, neighbourhood=props.def_n, level=0, relation_types=props.relation_types):
        """
        Retrieving users from twitter and reflect to our model.
        retrieve user and some of him neighbourhood in graph model by retrieving his relations (foll,friends,mentions)
        process user used for functions.py file

        input: start_user - is tweepy user obj or simple name
        by_what - is parameter of create_user func. [followers,friends]
        """
        log.info("\n>\nstart scrap user: %s" % start_user)
        try:
            #verifying user
            if self.db.verify_user(self._get_name_from_user(start_user)).status == m_user_status.s_updated:
                log.info("this user: %s is updated... skip him" % start_user)
                return
                #get his info and etc
            user_info = self.get_user_info(start_user)
            if not user_info:
                log.warn('after get his info - this none')
                return
                #saving user
            user_to_save = user_info.serialise()
            self.db.save_user(user_to_save)

            log.info('\n<scrapped user: %s\n<at neigh: %s in level: %s\n--------------------' %
                     ('\n'.join([str(item) for item in user_to_save.items()]), neighbourhood, level))

            #forming relations for this user, from cache and web

            if neighbourhood > level:
                relations = self._form_relations(user_info.name_,
                                                 relation_types,
                                                 user_info.get_relations())

                for r_type in relation_types:
                    for relation_object in relations[r_type]:
                        self.scrap(relation_object, neighbourhood, level=level + 1, relation_types=relation_types)

        except Exception as e:
            log.exception(e)
            log.warn('in scrapping exception as %s' % e)


    def diff_process(self):
        """
        at first you can have some users
        next - init_diff_machine - prepare users for difference analysing
        next start this method and get differences from db.diff_output (or at differences_users_output)
        """
        diff_users = self.db.get_users_for_diff()
        log.info('will load differences ')
        if not len(diff_users):
            log.info("no more users for differences")
        for i in range(len(diff_users)):
            try:
                user = diff_users[i]
                log.info('processing diffs for: %s' % user.name_)
                t_user = self._get_user_by_name(user.name_)
                m_user_now = self.get_user_info(t_user)
                if not m_user_now: log.warn('user now for diff is not load it is very bad.'); continue
                diff_factory = difference_factory()
                diff = diff_factory.create_difference(user_before=user, user_now=m_user_now)
                self.db.save_diffs(diff.serialise())

            except Exception as e:
                log.warn('some exception in e: %s' % e)
                log.exception(e)
                if 'Rate limit exceeded' in str(e):
                    log.info('ok, will be sleep...')
                    time.sleep(3600)











