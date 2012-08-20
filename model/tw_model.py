from datetime import datetime
from differences.diff_model import difference_element, m_hash_dict
from properties import props
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

    def serialise_from_db(self,dict):
        self.__dict__ = dict


if __name__ == '__main__':
    hash_dict1 = m_hash_dict({'one':'1','two':1})
    hash_dict2 = m_hash_dict({'one':'2'})

    hash_dict11 = m_hash_dict({'one':'1','two':1})
    print hash(hash_dict1), hash(hash_dict2)
    print hash_dict1 == hash_dict2

    print hash(hash_dict1), hash(hash_dict11)
    print hash_dict1 == hash_dict11
