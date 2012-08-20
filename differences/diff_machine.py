#todo create documentation
from differences.d_model import m_user_state_difference, difference_element, m_hash_dict
__author__ = 'Alesha'

def _prep_fields(fields, exclude):
        fields_ = [field for field in fields.items() if not exclude(field[0])]
        fields_ = dict(fields_)
        return fields_

def _validate_dict_of_array(array):
        if isinstance(array[0], dict) and not isinstance(array[0], m_hash_dict):
            return [m_hash_dict(el) for el in array]
        return array


def _diff_arrays(one_arr, two_arr):
        """
        forming difference element for arrays
        if return None - arrays are equals
        """
        so = set(_validate_dict_of_array(one_arr))
        st = set(_validate_dict_of_array(two_arr))

        if so == st:
            return None

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


def _diff_int(one_int, two_int):
        one_int = int(one_int)
        two_int = int(two_int)
        if max(one_int, two_int) == one_int:
            return difference_element(difference_element.s_stag, one_int - two_int)
        else:
            return difference_element(difference_element.s_grow, two_int - one_int)


def _diff_hz(o_value,value):
        return difference_element(difference_element.s_changed,
                            m_hash_dict({difference_element.s_a_old: o_value, difference_element.s_a_new: value}))



class difference_factory():
    """
    if you want to view differences in string create this object and call set_diff_process_function_(string_type,process_function)
    """
    def __init__(self):
        self.d_process_functions = []
        self.set_diff_process_function_(int,_diff_int)
        self.set_diff_process_function_(list,_diff_arrays)
        self.set_diff_process_function_(object,_diff_hz)

    def set_diff_process_function_(self,instance_obj,function):
        """
        function must be some function which return difference element and arguments have two similar type values
        like _diff_int or _diff_arrays
        """
        self.d_process_functions.append({'instance':instance_obj,'function':function})

    def create_user_difference(self,user_before, user_now, exclude=lambda x:str(x).endswith('_') or str(x).startswith('_')):
        """
        creating difference between two objects of user
        use it with m_users with similar names
        return m_difference object
        params: users, exclude - excluded fields as default it is: _fields_name and fields_name_
        use hashs as name - difference id is unique id of this difference will evaluate on the hashs of users
        """

        diff_id = {'left':hash(user_before),'right':hash(user_now)}

        difference = m_user_state_difference(diff_id,user_now.name_)

        fields_before = _prep_fields(user_before.__dict__, exclude)
        fields_now = _prep_fields(user_now.__dict__, exclude)


        #if some old field was removed:
        for field in fields_before:
            if not fields_now.has_key(field):
                was_removed = difference_element(state=difference_element.s_rem,
                                                 content={field, m_hash_dict(fields_before[field])})
                difference.set_field(field, was_removed)

        #if some new field added:
        for field in fields_now:
            if not fields_before.has_key(field):
                added = difference_element(state=difference_element.s_add, content=m_hash_dict({field, fields_now[field]}))
                difference.set_field(field, added)

        #for elements in now, in before - ignoring
        for self_element in fields_now.items():
            key = self_element[0]
            value = self_element[1]
            if key in fields_before.keys() and key in fields_now.keys():
                #prepearing old and new values
                o_value = fields_before[key]
                if o_value == value:
                    continue
                for inst_function in self.d_process_functions:
                    if isinstance(value,inst_function['instance']) and isinstance(o_value,inst_function['instance']):
                        diff_element = inst_function['function'](o_value,value)
                        if diff_element and diff_element[difference_element.d_content]:
                            difference.set_field(key, diff_element)

        return difference

