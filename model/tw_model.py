from datetime import datetime
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

class m_difference(serializable):
    def __init__(self,diff_id):
        self.diff_id = diff_id

class m_user_state_difference(m_difference):

    """
    Containing fields initialised in diff_machine packet. This fields like in user but with '_diff' suffix.
    Any field contains difference_element (like dict) with some difference state like this:
    {state:add, content:field_content} - added new field
    For example:
    friends_count: {state:grow, content:1} - new user difference about old on one friend
    """
    p_diff = '_diff'

    def __init__(self, diff_id, user_name=None):
        m_difference.__init__(self, diff_id)
        self.date_touch = datetime.now()
        self.user_name = user_name

    def set_field(self,name,content):
        self.__setattr__(name+self.p_diff,content)

    def get_field(self,name):
        return self.__getattribute__(name+self.p_diff)

    def is_field(self,name):
        return self.__dict__.has_key(name)


class difference_element(dict):
    """
    states and some methods for difference object element
    """

    s_rem = 'rem'
    s_add = 'add'
    s_grow = 'grow'
    s_stag = 'stag'
    s_no_grow = 'no grow'
    s_changed = 'changed'
    s_not_changed = 'not changed'
    s_a_new = 'new'
    s_a_old = 'old'
    s_a_intersect = 'intersect'
    d_state = 'state'
    d_content = 'content'

    def __init__(self, state, content, seq=[], **kwargs):
        dict.__init__(self, seq, **kwargs)
        self.add_element(state, content)

    def add_element(self, state, content):
        self[difference_element.d_state] = state
        self[difference_element.d_content] = content

    def add_arr_element(self, state, content):
        self[difference_element.d_content].append({difference_element.d_state: state, difference_element.d_content: content})
        return self

class m_hash_dict(dict):
    """
    wrapper for any dict in fields of user
    """
    def __init__(self, dict_,  **kwargs):
        dict.__init__(self, [], **kwargs)
        for el in dict_.items():
            self[el[0]] = el[1]

    def __hash__(self):
        return sum([hash(el[0])+hash(el[1]) for el in self.items()])

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else:
            for sel in self.items():
                if not other.has_key(sel[0]):
                    return False
                if other[sel[0]] != self[sel[0]]:
                    return False
        return True


if __name__ == '__main__':
    hash_dict1 = m_hash_dict({'one':'1','two':1})
    hash_dict2 = m_hash_dict({'one':'2'})

    hash_dict11 = m_hash_dict({'one':'1','two':1})
    print hash(hash_dict1), hash(hash_dict2)
    print hash_dict1 == hash_dict2

    print hash(hash_dict1), hash(hash_dict11)
    print hash_dict1 == hash_dict11
