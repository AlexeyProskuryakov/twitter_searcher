__author__ = '4ikist'

class element(object):
    @staticmethod
    def get_start_stop(model_id_, add_object=None):
        start = element('#start#', 1, model_id_=model_id_, additional_obj=add_object, )
        stop = element('#stop#', 1, model_id_=model_id_, additional_obj=add_object, )
        return start, stop

    def __init__(self, content, weight, additional_obj=None, model_id_=None, ):
        """
        element which contain some content: if it node - n_gram of words, if it edge - from ind to ind
        weight - some his weight
        also additional object - added in message - some index of message, may be attribute that it was re tweet or another
        """
        self.content = content
        self.weight = weight

        if additional_obj:
            self.additional_obj = additional_obj
            #id of markov chain object
        self.model_id_ = model_id_
        #information for database

    def generate_mongo_id(self):
        self._id = hash(self.content) + hash(self.weight) + hash(
            self.model_id_) if self.model_id_ else 31

    def _get_id(self):
        return self._id

    def _set_id(self, id):
        self._id = id

    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other, element) and self.content == other.content:
            if element.__dict__.has_key('additional_obj') and other.__dict__.has_key('additional_obj'):
                if self.additional_obj == other.additional_obj:
                    return True
                else: return False
            return True
        return False

    def __repr__(self):
        return self.content, self.weight

    def __str__(self):
        return str(self.content) + ':' + str(self.weight)

    def increment(self, value):
        self.weight += value

    def set_fields(self, fields):
        for field in fields.items():
            self.__dict__[field[0]] = field[1]

    def _serialise(self):
        return self.__dict__

    @staticmethod
    def create(dict, relation_create=False):
        if relation_create:
            el = relation(dict['content'], dict['weight'],
                          model_id_=dict['model_id_'])
        else:
            el = element(dict['content'], dict['weight'],
                         model_id_=dict['model_id_'])

        el._id = dict['_id']
        if dict.has_key('additional_object'):
            el.additional_obj = dict['additional_object']
        return el

    @staticmethod
    def equals(element1, element2):
        if isinstance(element1, element) and isinstance(element2, element) and element1.__dict__ == element2.__dict__:
            return True
        return False


class relation(element):
    def __init__(self, content, weight, additional_obj=None, model_id_=None):
        element.__init__(self, content, weight, additional_obj, model_id_)
        self.from_ = content[0]
        self.to_ = content[1]

    def _get_adjacent(self, id):
        if self.content[0] == id:
            return {'id': self.content[1], 'state': 'to_this'}
        elif self.content[1] == id:
            return {'id': self.content[0], 'state': 'from_this'}