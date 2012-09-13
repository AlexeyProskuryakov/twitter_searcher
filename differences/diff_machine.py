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

    note: any object must have similar by type elements in similar fields

    see: create differences
    """

    def __init__(self, exclude=None, form_id=None, process_ifunctions=None):
        if not exclude:
            self.exclude = lambda x:str(x).endswith('_') or str(x).startswith('_')
        if not form_id:
            self.form_id = lambda x:{'left': x[0], 'right': x[1]}
        if not process_ifunctions:
            self.process_ifunctions = [
                    {'instance': int, 'function': difference_factory.diff_int},
                    {'instance': str, 'function': difference_factory.diff_str},
                    {'instance': list, 'function': difference_factory.diff_arrays},
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

    def _field_intersection_difference(self,difference,fields_now,fields_before):
        intersection = set(fields_now).intersection(set(fields_before))
        for field_element_key in intersection:
                #prepearing old and new values
            value_now = fields_now[field_element_key]
            value_before = fields_before[field_element_key]

            if difference_factory._equals(value_now, value_before):
                continue
                        #for functions and their instances in process functions
            for if_function in self.process_ifunctions:
                if isinstance(value_now, if_function['instance']) and isinstance(value_before, if_function['instance']):
                    diff_element = if_function['function'](o_value, value)
                    if diff_element and diff_element[difference_element.d_content]:
                            diff_element.field_type = if_function['instance']
                            diff_element.field_diff_function = if_function['function']
                            difference.set_field(field_element_key, diff_element)
        return difference

    def _field_symmetric_difference(self,difference,fields_now,fields_before):

        keys_of_fields_before = set(fields_before.keys())
        keys_of_fields_now = set(fields_now.keys())

        symmetric_difference = keys_of_fields_before.symmetric_difference(keys_of_fields_now)
        union = keys_of_fields_before.union(keys_of_fields_now)

        for field in symmetric_difference:
                diff_state = 'can_not_diff_by_this'
                difference_element = difference_element(state=diff_state,content=None)
                added.field_type = type(fields_before[field])
                added.field_diff_function = self._field_symmetric_difference()
                difference.set_field(field, added)

        return difference

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
        #forming fields like m_hash_dicts, like a dict but can be hashable and have set of k:v
        fields_before = difference_factory._prep_fields(user_before.__dict__, self.exclude)
        fields_now = difference_factory._prep_fields(user_now.__dict__, self.exclude)

        #process fields for their symmetric difference
        difference = self._field_symmetric_difference(difference,fields_now,fields_before)

        #process fields by their intersection
        difference = self._field_symmetric_difference(difference,fields_now,fields_before)

        #if difference has not diff_fields exclude admin difference fields
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
        fields_ = m_hash_dict(dict(fields_))
        return fields_

    @staticmethod
    def _validate_dict_of_array(array):
        if len(array) and isinstance(array[0], dict) and not isinstance(array[0], m_hash_dict):
            return [m_hash_dict(el) for el in array]
        return array



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
    def diff_arrays(one_arr, two_arr):
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
            de = difference_element(difference_element.s_rem, [],None,difference_factory.diff_int)
        if ladded_in_new:
            de = difference_element(difference_element.s_add, [],None,difference_factory.diff_int)

        if len(added_in_new):
            de.add_arr_element(difference_element.s_a_new, difference_factory.__destruct_h_set(added_in_new))
        if len(was_in_old):
            de.add_arr_element(difference_element.s_a_old, difference_factory.__destruct_h_set(was_in_old))
        if len(int):
            de.add_arr_element(difference_element.s_a_intersect, difference_factory.__destruct_h_set(int))

        return de


    @staticmethod
    def diff_int( one_int, two_int):
        one_int = int(one_int)
        two_int = int(two_int)
        if one_int == two_int:
            return difference_element(difference_element.s_no_grow, None,difference_factory.diff_int)
        elif max(one_int, two_int) == one_int:
            return difference_element(difference_element.s_stag, one_int - two_int,difference_factory.diff_int)
        else:
            return difference_element(difference_element.s_grow, two_int - one_int,difference_factory.diff_int)

    @staticmethod
    def diff_str(element1, element2):
        difference_element(difference_element.s_changed,
                           m_hash_dict({difference_element.s_a_old: element1, difference_element.s_a_new: element2}))


    @staticmethod
    def __print_difference(m_difference):
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
    print set(m_hash_dict({1:1,2:2,3:4}))
#    diff = difference_factory.diff_arrays([[1, 1], 1, 1, 1, [1, 1]], [2, [2, 2], 2, [2, 2]])
#    print diff