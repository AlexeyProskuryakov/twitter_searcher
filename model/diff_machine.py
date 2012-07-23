from datetime import datetime
from model.exceptions import model_exception
from model.tw_model import user
from properties import props

__author__ = 'Alesha'
p_diff = '_diff'

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

#todo refactor! create difference object and difference machine. this arch is bad!
class difference_element(dict):
    def __init__(self, state, content, seq=[], **kwargs):
        dict.__init__(self, seq, **kwargs)
        self.add_element(state, content)

    def add_element(self, state, content):
        self[d_state] = state
        self[d_content] = content

    def add_arr_element(self, state, content):
        self[d_content].append({d_state: state, d_content: content})
        return self


class difference(user):
    def __init__(self, one, two):
        if type(one) != type(two) != type(super):
            raise model_exception('can not have difference with not user')
        self.name = one.name
        user.__init__(self, str(self.name))
        self.fill_difference(one, two)

    def get_state_by_field_name(self, name):
        return self.__dict__[name + p_diff][d_state]

    def get_all_content_by_field_name(self, name):
        return self.__dict__[name + p_diff][d_content]

    def fill_difference(self, one, two):
        o_dict = one.__dict__
        t_dict = two.__dict__

        list_type = type(list())
        int_type = type(int(0))
        for self_element in self.__dict__.items():
            key = self_element[0]
            value = self_element[1]
            if key in o_dict.keys() and key in t_dict.keys():
                o_value = o_dict[key]
                t_value = t_dict[key]
                #if type of all attribute is array
                if type(o_value) == type(t_value) == list_type == type(value):
                    diff_element = self.diff_arrays(o_dict[key], t_dict[key])
                #for integers parameters
                elif type(o_value) == type(t_value) == int_type:
                    diff_element = self.diff_int(o_value, t_value)
                #for date
                elif 'date_touch' in str(key):
                    diff_element = difference_element("touch", datetime.now().strftime(props.time_format))
                #for another parameters...
                elif o_value != t_value:
                    diff_element = difference_element(s_changed, {'old': o_value, 'new': t_value})
                elif o_value[-1]=='_':
                    continue
                else:
                    diff_element = difference_element(s_not_changed, None)
                self.__setattr__(str(key) + p_diff, diff_element)

    def diff_arrays(self, one_arr, two_arr):
        so = set(one_arr)
        st = set(two_arr)

        if st == so:
            return difference_element(s_no_grow, None)
        else:
            int = so.intersection(st)
            was_in_old = so.difference(int)
            lwas_in_old = len(was_in_old)

            added_in_new = st.difference(int)
            ladded_in_new = len(added_in_new)

            de = None
            if lwas_in_old:
                de = difference_element(s_rem, [])
            if ladded_in_new:
                de = difference_element(s_add, [])

            de.add_arr_element(s_a_new, list(added_in_new))
            de.add_arr_element(s_a_old, list(was_in_old))
            de.add_arr_element(s_a_intersect, list(int))
            return de


    def diff_int(self, one_int, two_int):
        one_int = int(one_int)
        two_int = int(two_int)
        if one_int == two_int:
            return difference_element(s_no_grow, None)
        elif max(one_int, two_int) == one_int:
            return difference_element(s_stag, one_int - two_int)
        else:
            return difference_element(s_grow, two_int - one_int)


    def serialise(self):
        return dict(
            [
            (element[0], element[1]) for element in self.__dict__.items()
                                     if str(element[0]).endswith(p_diff) or
                                        str(element[0]).endswith("name")
            ]
        )