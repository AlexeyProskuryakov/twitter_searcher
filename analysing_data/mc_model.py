__author__ = '4ikist'


class graph_object(object):
    def __init__(self, model_id_, weight):
        self.weight = weight
        self.model_id_ = model_id_

    def increment(self, value):
        self.weight += value

    def set_fields(self, fields):
        for field in fields.items():
            self.__dict__[field[0]] = field[1]

    def serialise(self):
        result = {}
        for el in self.__dict__.keys():
            content = self.__dict__[el]
            if content:
                result[el] = content
        return result


class node(graph_object):
    def __init__(self, content, weight, model_id_, _id=None):
        """
        element which contain some content: if it node - n_gram of words, if it edge - from ind to ind
        weight - some his weight
        also additional object - added in message - some index of message, may be attribute that it was re tweet or another
        """
        super(node, self).__init__(model_id_, weight)
        self.content = content
        self._id = _id

    def __hash__(self):
        if isinstance(self.content, list):
            return sum([hash(el) for el in self.content])
        return hash(self.content)

    def __eq__(self, other):
        if isinstance(other, node) and self.content == other.content:
            return True
        return False

    def __str__(self):
        return repr(self.content) + ':' + str(self.weight)

    def repr(self):
        return self.__str__()

    @staticmethod
    def equals(element1, element2):
        if isinstance(element1, node) and isinstance(element2, node) and element1.__dict__ == element2.__dict__:
            return True
        return False


class relation(graph_object):
    def __init__(self, from_, to_, weight, model_id_):
        super(relation, self).__init__(model_id_, weight)
        self.from_ = from_
        self.to_ = to_

    def _get_adjacent(self, id):
        if self.from_ == id:
            return self.to_
        elif self.to_ == id:
            return self.from_
