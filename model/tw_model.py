from datetime import datetime
<<<<<<< HEAD
from differences.d_model import m_hash_dict
=======
from differences.diff_model import difference_element, m_hash_dict
from properties import props
>>>>>>> ec059c5dc6053cc3b66b865533c4d3e926995199
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
    s_saved = 'saved'
    s_update_needed = 'update_needed'
    s_updated = 'update'

    def __init__(self,status,last_diff = None):
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
        self.list_count = None
        self.tweets_stat = None #statistic of user perls
        self.timeline = None
        self.lists_names = None
        self.timeline_count = None
        self.protected = None

        self.favorites = None

    def set_hash_tags(self,hash_tags):
        """
        initialize and settings up all hash tags which user was said
        """
        self.hash_tags = hash_tags

    def set_relations(self,dict_of_relations):
        """
        relations must be like that:
        dict_of_relations = {'followers':[names], 'friends':[names],'mentions':[names]},
        """
        self.followers_relations = dict_of_relations['followers']
        self.friends_relations = dict_of_relations['friends']
        self.mention_relations = dict_of_relations['mentions']

<<<<<<< HEAD
    def __hash__(self):
        return self.followers_count+\
               self.friends_count+\
               self.timeline_count+\
                len(self.mention_relations)+\
                hash(self.real_name)+\
                hash(self.date_touch_)

=======
    def serialise_from_db(self,dict):
        self.__dict__ = dict
>>>>>>> ec059c5dc6053cc3b66b865533c4d3e926995199


    def serialise_from_db(self,dict):
        self.__dict__ = dict
