from datetime import datetime


__author__ = 'Alesha'

class m_difference(object):
    """
    Containing fields initialised in diff_machine packet. This fields like in user but with '_diff' suffix.
    Any field contains difference_element (like dict) with some difference state like this:
    {state:add, content:field_content} - added new field
    For example:
    friends_count: {state:grow, content:1} - new user difference about old on one friend

    note #!mind i want to create difference model/
     and it may be that: m_diff(another_m_diff_left, another_m_diff_right) = m_another_yet_diff_!_(_v_rot_mne_nogi_)_)

    """
    #for difference fields names and in there have types @see difference_element
    fp_diff = '_diff'

    def __init__(self,diff_id_):
        #contains fields of
        self.diff_id_ = diff_id_

    def set_field(self,name,content):
        self.__setattr__(name+self.fp_diff,content)

    def get_field(self,name):
        return self.__getattribute__(name+self.fp_diff)

    def is_field(self,name):
        return self.__dict__.has_key(name)

    def serialise(self):
        return self.__dict__


    def has_diff_fields(self):
        """
        returns true if this object contains difference fields
        """
        keys = self.__dict__.keys()
        for key in keys:
            s_key = str(key)
            if s_key.endswith(m_difference.fp_diff):
                return True

        return False


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

class difference_element(m_hash_dict):
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


    def __init__(self, state, content, seq=[], field_type = None, **kwargs):
        dict.__init__(self, seq, **kwargs)
        self.add_element(state, content)
        if not field_type:
            self.field_type = difference_element

    def add_element(self, state, content):
        self[difference_element.d_state] = state
        self[difference_element.d_content] = content

    def add_arr_element(self, state, content):
        self[difference_element.d_content].append({difference_element.d_state: state, difference_element.d_content: content})
        return self



