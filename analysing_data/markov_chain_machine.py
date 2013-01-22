from analysing_data.booster import create_node
from analysing_data.redis_handlers import model_handler
from analysing_data.mc_model import node, relation
import loggers
from visualise.markov_chain_visualise import mc_vis
import networkx as nx

__author__ = 'Alesha'

log = loggers.logger

class markov_chain(object):
    def __init__(self, model_id_, model_handler=model_handler(), n_of_gram_=1):
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
        self.handler = model_handler
        self._id = model_id_
        self.graph = nx.DiGraph()
        self.words_count = 0

    def add_message(self, message):
        """
        message must be list of words
        """
        #processing nodes
        elem_ids = []
        message_len = len(message)
        for i in range(0, message_len):
            if i + self.n_of_gram_ <= message_len:
                elem = node(message[i:i + self.n_of_gram_], 1, self.model_id_)
                elem_id = self.handler.add_node_or_increment(elem)
                elem_ids.append(elem_id)
                #processing relations
        len_ids = len(elem_ids)
        for i in range(len_ids):
            if i + 1 < len_ids:
                rel = relation(elem_ids[i], elem_ids[i + 1], 1, model_id_=self.model_id_)
                self.handler.add_relation_or_increment(rel)

        self.words_count += len_ids


    def get_model_weight(self):
        return len(self.handler.get_nodes(self.model_id_))


    def get_nodes(self):
        return self.handler.get_nodes(self.model_id_)

    def get_relation_weight(self, from_id, to_id):
        return self.handler.get_relation_weight(from_id, to_id)

    def visualise(self, buff_size):
        nodes = self.get_nodes()
        relations = self.handler.get_relations()
        len_nodes = len(nodes)
        len_relations = len(relations)
        for i in range(0, len_nodes, buff_size):
            log.info('add nodes...%s -> %s all (%s)' % (i, i + buff_size, len_nodes))
            if i + buff_size < len_nodes:
                mc_vis.put_mc_nodes(nodes[i:i + buff_size])
            else:
                mc_vis.put_mc_nodes(nodes[i:])

        for i in range(0, len_relations, buff_size):
            log.info('add relations...%s -> %s all (%s)' % (i, i + buff_size, len_relations))
            if i + buff_size < len_relations:
                mc_vis.put_mc_relations(relations[i:i + buff_size])
            else:
                mc_vis.put_mc_relations(relations[i:])

    def get_nx_graph(self):
        if not self.graph:
            self.graph = nx.DiGraph()
            for node in self.get_nodes():
                self.graph.add_node(node._id, {'content': node.content, 'weight': node.weight})

                for rel in self.handler.get_relations(node._id, self.model_id_):
                    self.graph.add_edge(rel.from_, rel.to_, {'weight': rel.weight})

        return self.graph

    def print_me(self):
        log.info('\n\n-------------%s' % self.model_id_)
        nodes = self.get_nodes()
        for node in nodes:
            log.info('\n---------------node: %s %s [%s]' % (node.content, node.weight, node._id))

            edges = self.handler.get_relations(node._id, self.model_id_)
            for edge in edges:
                log.info('%s --- %s --- %s' % (
                    self.handler.get_node(edge.from_, self.model_id_).content, edge.weight,
                    self.handler.get_node(edge.to_, self.model_id_).content))

#    def get_betweenness_centrality(self):
#        filled = nx.algorithms.betweenness_centrality(self.graph)
#        nodes = []
#        for el in filled:
#            node = self.get_node_by_id(el)
#            nodes.append({})
#


def create_model(messages, model_id, booster):
    mc = markov_chain(model_id, booster)
    for message in messages:
        mc.add_message(message)
    return mc