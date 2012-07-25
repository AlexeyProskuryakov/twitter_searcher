from datetime import datetime
from model.exceptions import model_exception
from model.tw_model import m_user, m_difference, difference_element
from properties import props

__author__ = 'Alesha'


def create_difference(user_before, user_now, exclude=lambda x:str(x).endswith('_')):
    """
    creating difference between two objects of user
    use it with m_users with similar names
    return m_difference object
    """
    if type(user_before) != type(user_now) != type(m_user('')):
        raise model_exception('can not have difference with not user')
    if user_before.name_ != user_now.name_:
        raise model_exception('can not have difference between users with differences names')

    fields_before = user_before.__dict__
    fields_now = user_now.__dict__

    difference = m_difference(user_now.name_)
    #if some old field was removed:
    for field in fields_before:
        if not fields_now.has_key(field):
            was_removed = difference_element(state=difference_element.s_rem, content={field, fields_before[field]})
            difference.set_field(field , was_removed)

    #if some new field added:
    for field in fields_now:
        if not fields_before.has_key(field):
            added = difference_element(state=difference_element.s_add, content={field, fields_now[field]})
            difference.set_field(field , added)

    #for elements in now in before - ignoring
    for self_element in fields_now.items():
        key = self_element[0]
        value = self_element[1]
        if key in fields_before.keys() and key in fields_now.keys():
            #prepearing old and new values
            o_value = fields_before[key]
            n_value = fields_now[key]
            #if exclude
            if exclude(key):
                continue

            #if type of field is array
            if type(o_value) == type(n_value) == type(list()) == type(value):
                diff_element = diff_arrays(fields_before[key], fields_now[key])

            #if type is integer
            elif type(o_value) == type(n_value) == type(int(0)):
                diff_element = diff_int(o_value, n_value)

            #for another parameters...
            elif o_value != n_value:
                diff_element = difference_element(difference_element.s_changed, {'old': o_value, 'new': n_value})
            else:
                continue

            difference.set_field(key, diff_element)

    return difference


def diff_arrays( one_arr, two_arr):
    """
    for array elements s_a_ states
    for di
    """
    so = set(one_arr)
    st = set(two_arr)

    if st == so:
        return difference_element(difference_element.s_no_grow, None)
    else:
        int = so.intersection(st)
        was_in_old = so.difference(int)
        lwas_in_old = len(was_in_old)

        added_in_new = st.difference(int)
        ladded_in_new = len(added_in_new)

        de = None
        if lwas_in_old:
            de = difference_element(difference_element.s_rem, [])
        if ladded_in_new:
            de = difference_element(difference_element.s_add, [])
        if len(added_in_new):
            de.add_arr_element(difference_element.s_a_new, list(added_in_new))
        if len(was_in_old):
            de.add_arr_element(difference_element.s_a_old, list(was_in_old))
        if len(int):
            de.add_arr_element(difference_element.s_a_intersect, list(int))
        return de


def diff_int( one_int, two_int):
    one_int = int(one_int)
    two_int = int(two_int)
    if one_int == two_int:
        return difference_element(difference_element.s_no_grow, None)
    elif max(one_int, two_int) == one_int:
        return difference_element(difference_element.s_stag, one_int - two_int)
    else:
        return difference_element(difference_element.s_grow, two_int - one_int)


