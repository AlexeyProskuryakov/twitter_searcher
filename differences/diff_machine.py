from differences.d_model import difference_element, m_hash_dict, m_difference
from model.tw_model import m_user
import tools
from loggers import logger

__author__ = 'Alesha'

log = logger

class difference_factory():
    """
    exclude - excluded fields as default it is: _fields_name and fields_name_
    hash_f - hash_function which form diff_id_
    process_ifunctions - functions which process values and instances which flags functions do their work

    if you want to create difference process function create it with some instance
    for example:
    {instance:int,function:some_int_function}
    if value of some field in object will be int
    some_int_function will process this values in both difference objects
    some_int_function must input values and return difference element (see d_model.py)
    for integrate your some_int_function use add_process_i_function

    note: any object must have unique elements in similar fields

    see: create differences
    """

    def __init__(self, exclude=None, form_id=None, process_ifunctions=None):
        if not exclude:
            self.exclude = lambda x:str(x).endswith('_') or str(x).startswith('_')
        if not form_id:
            self.form_id = lambda x:{'left': x[0], 'right': x[1]}
        if not process_ifunctions:
            self.process_ifunctions = [
                    {'instance': int, 'function': difference_factory._diff_int},
                    {'instance': str, 'function': difference_factory._diff_hz},
                    {'instance': list, 'function': difference_factory._diff_arrays},
            ]

    def add_process_i_function(self, instance, function):
        self.process_ifunctions.append({'instance': instance, 'function': function})


    def _get_diff_id_(self, ul, ur):
        diff_id_ = None
        try:
            left_part = ul.get_diff_part_id()
            right_part = ur.get_diff_part_id()
            diff_id_ = self.form_id((left_part, right_part))
        except Exception as e:
            log.exception(e)
            log.warn('i have some objects which have not get_diff_part_id() method... %s > %s' % (ul, ur))
            raise e

        return diff_id_

    def _hash_fields(self, ul, ur):
        for i in ul.__dict__.iteritems():
            key = i[0]
            value = i[1]


    def create_difference(self, user_before, user_now):
        """
        creating difference between two objects of user or another objects which in list_of_instances
        return m_difference object
        params: users
        use hashs as id - difference id is unique id of this difference will evaluate on the hashs of users
        /and in data base it will be good...
        if hashes of objects are equals - returning None
        raises exception if bad instances of objects
        """

        if hash(user_before) == hash(user_now):
            log.info('no any differences between users %s > %s' % (user_before, user_now))
            return None
        diff_id_ = self._get_diff_id_(user_before, user_now)
        difference = m_difference(diff_id_)

        fields_before = difference_factory._prep_fields(user_before.__dict__, self.exclude)
        fields_now = difference_factory._prep_fields(user_now.__dict__, self.exclude)


        #if some old field was removed:
        for field in fields_before:
            if not fields_now.has_key(field):
                was_removed = difference_element(state=difference_element.s_rem,
                                                 content={field, m_hash_dict(fields_before[field])})
                was_removed.field_type = field
                difference.set_field(field, was_removed)

        #if some new field added:
        for field in fields_now:
            if not fields_before.has_key(field):
                added = difference_element(state=difference_element.s_add,
                                           content=m_hash_dict({field, fields_now[field]}))
                added.field_type = field
                difference.set_field(field, added)

        #for elements in now in before - ignoring
        for self_element in fields_now.items():
            key = self_element[0]
            value = self_element[1]
            if key in fields_before.keys() and key in fields_now.keys():
                #prepearing old and new values
                o_value = fields_before[key]

                if difference_factory._equals(value, o_value):
                    continue

                    #for functions and their instances in process functions
                for if_function in self.process_ifunctions:
                    if isinstance(value, if_function['instance']) and isinstance(o_value, if_function['instance']):
                        diff_element = if_function['function'](o_value, value)
                        if diff_element and diff_element[difference_element.d_content]:
                            diff_element.field_type = key
                            difference.set_field(key, diff_element)
        #if difference has diff_fields exclude admin difference fields
        if not difference.has_diff_fields():
            log.info("no difference fields in difference")
            return None

        return difference

    @staticmethod
    def _equals(one, two):
        if isinstance(one, list) and isinstance(two, list) and len(one) == len(two):
            one = difference_factory._validate_dict_of_array(one)
            two = difference_factory._validate_dict_of_array(two)
            for one_el in one:
                if one_el not in two:
                    return False
            return True

        elif isinstance(one, dict) and isinstance(two, dict) and len(one) == len(two):
            two_values = two.values()
            for one_el in one.items():
                if not two.has_key(one_el[0]) or not one_el[1]in two_values:
                    return False
            return True

        elif one == two:
            return True
        else:
            return False


    @staticmethod
    def _prep_fields(fields, exclude):
        fields_ = [field for field in fields.items() if not exclude(field[0])]
        fields_ = dict(fields_)
        return fields_

    @staticmethod
    def _validate_dict_of_array(array):
        if len(array) and isinstance(array[0], dict) and not isinstance(array[0], m_hash_dict):
            return [m_hash_dict(el) for el in array]
        return array

    @staticmethod
    def _diff_hz(element1, element2):
        difference_element(difference_element.s_changed,
                           m_hash_dict({difference_element.s_a_old: element1, difference_element.s_a_new: element2}))


    @staticmethod
    def __create_h_set(array):
        result = h_set()

        for el in array:
            if isinstance(el, list):
                result.add(difference_factory.__create_h_set(el))
            else:
                result.add(el)
        return result

    @staticmethod
    def __destruct_h_set(array):
        result = list()
        for el in array:
            if isinstance(el, h_set):
                result.append(difference_factory.__destruct_h_set(el))
            else:
                result.append(el)
        return result

    @staticmethod
    def _diff_arrays(one_arr, two_arr):
        """
        for array elements s_a_ states
        """
        if not len(one_arr) or not len(two_arr):
            return None

        #todo create set of some object which has equals method
        vdo = difference_factory._validate_dict_of_array(one_arr)
        vdt = difference_factory._validate_dict_of_array(two_arr)
        so = difference_factory.__create_h_set(vdo)
        st = difference_factory.__create_h_set(vdt)

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
            de.add_arr_element(difference_element.s_a_new, difference_factory.__destruct_h_set(added_in_new))
        if len(was_in_old):
            de.add_arr_element(difference_element.s_a_old, difference_factory.__destruct_h_set(was_in_old))
        if len(int):
            de.add_arr_element(difference_element.s_a_intersect, difference_factory.__destruct_h_set(int))
        return de


    @staticmethod
    def _diff_int( one_int, two_int):
        one_int = int(one_int)
        two_int = int(two_int)
        if one_int == two_int:
            return difference_element(difference_element.s_no_grow, None)
        elif max(one_int, two_int) == one_int:
            return difference_element(difference_element.s_stag, one_int - two_int)
        else:
            return difference_element(difference_element.s_grow, two_int - one_int)


    @staticmethod
    def print_difference(m_difference):
        if not m_difference:
            print None
            return
        dict = m_difference.__dict__
        for item in dict.items():
            print item


class h_set(set):
    def __hash__(self):
        hashes = []
        for x in self:
            hashes.append(hash(x))
        return sum(hashes)

if __name__ == '__main__':
    diff = difference_factory._diff_arrays([[1, 1], 1, 1, 1, [1, 1]], [2, [2, 2], 2, [2, 2]])
    print diff