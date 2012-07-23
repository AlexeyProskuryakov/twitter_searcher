from datetime import datetime
from properties import props

__author__ = '4ikist'

s_none = 'none'
s_saved = 'saved'

class m_user_status(object):
    def __init__(self,status,last_diff = None):
        self.status = status
        self.last_diff = last_diff



class m_user(object):

    def __init__(self, name):
        self.date_touch = datetime.now()
        self.name = name
        self.real_name = None
        self.followers_count = None
        self.friends_count = None
        self.list_count = None
        self.tweets_stat = None #statistic of user perls
        self.timeline = None
        self.lists_names = None
        self.timeline_count = None
        self.protected = None
        self.initted_ = None

        self.diffs = None

    def serialise(self):
        return self.__dict__

    def set_relations(self,dict_of_relations):
        self.followers_relations = dict_of_relations['followers']
        self.friends_relations = dict_of_relations['friends']
        self.mention_relations = dict_of_relations['mentions']



