from analysing_data.booster import db_booster
from analysing_data.mc_model import element
import loggers

__author__ = 'Alesha'

log = loggers.logger

class markov_chain(object):
    state = ['saved', 'not_saves']

    @staticmethod
    def create(model_id_, db_booster):
        mc = markov_chain(model_id_,db_booster)
        mc.__load()
        return mc

    def __init__(self, model_id_, db_booster, n_of_gram_=1):
        """
        note: message must be a list of words.
        input parameters: list of words and n which any node will be at parameter n_of_gram_ms
        for ex: if n_of_gram_ms will be 3 than
        mc of a,b,c,d will be
        (a,b,c),1/2 --- 1 ---> (b,c,d),1/2
        with relations count is len of (list of words) -- n and with plus - is count of words/
        count of unique words/relations see: len(obj.words/relations)
        
        you must create this model at data base engine.
        """
        self.n_of_gram_ = n_of_gram_
        self.model_id_ = model_id_
        self.db = db_booster
        self._id = model_id_

        saved = self.db.get_model_parameters(model_id_)
        if saved:
            self.words_count_ = saved['words_count_']
            self.relations_count_ = saved['relations_count_']

        else:
            self.words_count_ = 0
            self.relations_count_ = 0

        self.state = markov_chain.state[1]

    def save(self):
        self.state = markov_chain.state[0]
        self.db.add_model({'words_count_': self.words_count_, 'relations_count_': self.relations_count_,
                           'model_id_': self.model_id_, 'n_of_gramm': self.n_of_gram_, 'include': self.include})

    def __load(self):
        parameters = self.db.get_model_parameters(self.model_id_)
        new_dict = self.__dict__
        for params in parameters.items():
            new_dict[params[0]] = params[1]
        self.__dict__ = new_dict

    def add_message(self, message, additional_object=None):
        """
        message must be list of words
        """
        #cheking about saved state of model
        if self.state == markov_chain.state[0]:
            self.state = markov_chain.state[1]
            #generationg start and stop nodes
        start_node, stop_node = element.get_start_stop(self.model_id_, additional_object)
        prev_id = self.db.add_node_or_increment(start_node)
        last_id = self.db.add_node_or_increment(stop_node)

        message_len = len(message)
        for i in range(message_len):
            el = message[i]
            elem = element(el, 1, additional_object, self.model_id_)
            element_id = self.db.add_node_or_increment(elem)

            relation = element((prev_id, element_id), 1, additional_object, self.model_id_)
            self.db.add_relation_or_increment(relation)
            prev_id = element_id

            if i + 1 == message_len:
                relation = element((prev_id, last_id), 1, additional_object, self.model_id_)
                self.db.add_relation_or_increment(relation)

        self.words_count_ += len(message)
        self.relations_count_ = self.words_count_ - 1
        self.include = []

    def get_node_by_id(self, id):
        return element.create(self.db.nodes.find_one({'_id': id}))

    def get_nodes(self):
        return self.db.get_nodes(self.model_id_)

    def get_relations(self):
        return self.db.get_relations(self.model_id_)

    def get_relations_by_node_id(self, id, from_=False, to_=False):
        relations = []
        if from_:
            relations.extend(self.db.get_relations_from(id, model_id=self.model_id_))
        if to_:
            relations.extend(self.db.get_relations_to(id, model_id=self.model_id_))
        return relations

    def print_me(self):
        log.info('nodes: %s' % self.words_count_)
        nodes = self.get_nodes()
        for node in nodes:
            log.info(node)
        log.info('edges: %s' % self.relations_count_)
        edges = self.get_relations()
        for edge in edges:
            log.info('%s ---> %s ---> %s' % (
                self.get_node_by_id(edge.content[0]), edge.weight, self.get_node_by_id(edge.content[1])))

    def visualise(self,vis_processor):
        nodes = self.get_nodes()
        relations = self.get_relations()
        for node in nodes:
            vis_processor.put_mc_node(node)
        for rel in relations:
            vis_processor.put_mc_edge(rel)
