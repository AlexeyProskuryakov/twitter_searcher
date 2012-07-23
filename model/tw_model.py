from datetime import datetime
from properties import props

__author__ = '4ikist'



class user(object):

    def __init__(self, name):
        self.date_touch = datetime.now().strftime(props.time_format)
        self.name = '@'+name
        self.followers_count = 0
        self.friends_count = 0
        self.list_count = 0

        self.tweets_stat = [] #statistic of user perls
        self.timeline = []
        self.lists_names = []
        self.timeline_count = 0
        self.protected = False
        self.initted_ = None

    def serialise(self):
        return self.__dict__

    def __str__(self):
        return '\n'.join(self.serialise())


    def set_relations(self,dict_of_relations):
        self.followers_relations = dict_of_relations['followers']
        self.friends_relations = dict_of_relations['friends']
        self.mention_relations = dict_of_relations['mentions']



