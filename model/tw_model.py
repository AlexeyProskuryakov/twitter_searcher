from datetime import datetime
from differences.d_model import m_hash_dict
from model import functions

followers = 'followers'
friends = 'friends'
mentions = 'mentions'

__author__ = '4ikist'

class serializable(object):
    """
    object which serialize into db and deserialize
    """

    def serialise(self):
        return m_hash_dict(self.__dict__)


class m_user_status(serializable):
    """
    object of status from db
    """
    s_none = 'none'
    s_update_needed = 'update_needed'
    s_updated = 'update'

    def __init__(self, status, last_diff=None):
        self.status = status
        self.last_diff = last_diff


class m_user(serializable):
    """
    representing user in our model
    """


    @staticmethod
    def create(dict):
        user = m_user(dict['name_'])
        user.serialise_from_db(dict)
        return user

    def __init__(self, name):
        self.date_touch_ = datetime.now()
        self.name_ = name
        self.inited_ = None
        self.diffs_ = []

        self.real_name = None
        self.followers_count = None
        self.friends_count = None
        self.timeline = None
        self.timeline_count = None
        self.protected = None
        self.favorites_count = None

        self.followers_relations = []
        self.friends_relations = []
        self.mentions_relations = []

    def set_lists(self, lists_names, count):
        self.lists_names = lists_names
        self.lists_count = count

    def get_relations(self):
        return {followers: self.followers_relations if self.__dict__.has_key('followers_relations') else [],
                friends: self.friends_relations if self.__dict__.has_key('friends_relations') else [],
                mentions: self.mentions_relations if self.__dict__.has_key('mention_relations') else []}

    def set_relations(self, dict_of_relations):
        """
        relations must be like that:
        dict_of_relations = {'followers':[names], 'friends':[names],'mentions':[names]},
        """
        self.followers_relations = dict_of_relations[followers]
        self.friends_relations = dict_of_relations[friends]

    def set_timeline_info(self, timeline_info):
        self.urls = timeline_info[functions.url]
        self.hash_tags = timeline_info[functions.hash_tag]
        self.mentions = timeline_info[functions.mention]
        #for mention relations
        if self.mentions:
            self.mentions_relations = [mention[0] for mention in self.mentions]
        self.words = timeline_info[functions.word]

    def get_diff_part_id(self):
        return {'name_': self.name_, 'inited_': self.inited_}


    def serialise_from_db(self, dict):
        self.__dict__ = dict
