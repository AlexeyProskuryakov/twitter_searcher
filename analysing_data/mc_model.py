__author__ = '4ikist'

class element(object):
    r_type = 'r'
    w_type = 'w'

    states = {'start': 0, 'stop': 1, 'node': 2}

    @staticmethod
    def get_start_stop(add_object,model_id_):
        start = element(('start',), 1, type=element.w_type, model_id_=model_id_, additional_obj=add_object,
                                  state=element.states['start'])
        stop = element(('stop',), 1, type=element.w_type, model_id_=model_id_, additional_obj=add_object,
                                state=element.states['stop'])
        start.mc_id = 0
        stop.mc_id = 1
        return start,stop

    def __init__(self, content, weight, type, additional_obj=None, model_id_=None, mc_id=None, state=states['node']):
        """
        element which contain some content: if it node - n_gram of words, if it edge - from ind to ind
        weight - some his weight
        also additional object - added in message - some index of message, may be attribute that it was re tweet or another
        """
        self.content = content
        self.weight = weight

        self.f_weight = None
        self.f_rel_weight = None

        self.additional_obj = additional_obj
        #id of markov chain object
        self.model_id_ = model_id_
        #id in words or relation list
        self.mc_id = mc_id

        #some additional information/
        self.type = type
        self.state = state
        #information for database
        self._id = None

    def generate_mongo_id(self):
        self._id = hash(self.content) + hash(self.weight) + hash(self.additional_obj) + hash(self.model_id_) if self.model_id_ else 31 + hash(self.mc_id) if self.mc_id else 42 + hash(self.type)

    def _get_id(self):
        return self._id

    def _set_id(self, id):
        self._id = id

    def __hash__(self):
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other, element) and self.content == other.content and self.additional_obj == other.additional_obj:
            return True
        return False

    def __repr__(self):
        return self.content, self.weight

    def __str__(self):
        return str(self.content) + ':' + str(self.weight)

    def increment(self, value):
        self.weight += value

    def set_fields(self,fields):
        for field in fields.items():
            self.__dict__[field[0]] = field[1]

    def _serialise(self):
        if not self._id:
            self.generate_mongo_id()
        return self.__dict__

    @staticmethod
    def create(dict):
        el = element(dict['content'], dict['weight'],
                     additional_obj=dict['additional_obj'],
                     model_id_=dict['model_id_'],
                     mc_id=dict['mc_id'],
                     state=dict['state'],
                     type=dict['type'])
        el._id = dict['_id']

        return el

    @staticmethod
    def equals(element1, element2):
        if isinstance(element1, element) and isinstance(element2, element) and element1.__dict__ == element2.__dict__:
            return True
        return False


