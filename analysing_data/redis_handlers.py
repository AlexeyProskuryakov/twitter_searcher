#coding:utf-8
import redis
from mc_model import node, relation, graph_object
from loggers import logger

log = logger
__author__ = '4ikist'

class model_handler(object):
    """
    handling model at three types:

    model_id : set[node_ids]
    node_id:model_id:rel : hset[node_id:weight]
    node_id:model_id:weight : node_weight
    node_id:model_id:content : node_content

    """
    node_rel = '%s:%s:rel'
    node_weight = '%s:%s:weight'
    node_content = '%s:content'


    def __init__(self, truncate=False, host='localhost', port=6379, db=0):
        super(model_handler, self).__init__()
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        if truncate:
            self.r.flushdb()

    def __generate_id(self, node):
        return hash(repr(node.content))

    def __get_content(self, node_id):
        content = self.r.get(self.node_content % (node_id))
        sem = content.index(':')
        element = content[:sem]
        type = content[sem+1:]
        if str(type) == str(type(unicode(
            
        ))):

            element = unicode(content, 'utf-8')
        return content

    def __set_content(self,node):
        content = node.content
        content_type = type(content)
        ser_content = '%s:%s'%(content,content_type)
        return ser_content

    def add_relation_or_increment(self, relation):
        name_from = self.node_rel % (relation.from_, relation.model_id_)
        name_to = self.node_rel % (relation.to_, relation.model_id_)

        if self.r.hexists(name_from, relation.to_):
            self.r.hincrby(name_from, relation.to_, relation.weight)
            self.r.hincrby(name_to, relation.from_, relation.weight)
        else:
            self.r.hset(name_from, relation.to_, relation.weight)
            self.r.hset(name_to, relation.from_, relation.weight)


    def add_node_or_increment(self, node):
        if not node._id:
            node._id = self.__generate_id(node)

        if self.r.sismember(node.model_id_, node._id):
            self.r.incr(self.node_weight % (node._id, node.model_id_), node.weight)
        else:
            self.r.sadd(node.model_id_, node._id)
            self.r.set(self.node_content % (node._id,), self.__set_content(node.content))
            self.r.set(self.node_weight % (node._id, node.model_id_), node.weight)
        return node._id


    def get_neighbours(self, node_id, model_id):
        rels = self.r.hgetall(self.node_rel % (node_id, model_id))
        nodes = []
        for rel in rels:
            r_node = self.get_node(rel, model_id)
            nodes.append(r_node)
        return nodes

    def get_nodes(self, model_id):
        nodes_elements = self.r.smembers(model_id)
        result = []
        for node_id in nodes_elements:
            r_node = self.get_node(node_id, model_id)
            result.append(r_node)
        return result

    def get_weight(self, model_id):
        return len(self.r.smembers(model_id))

    def get_node(self, node_id, model_id):
        weight = self.r.get(self.node_weight % (node_id, model_id))
        content = self.__get_content(node_id)
        r_node = node(content, weight, model_id, node_id)
        return r_node

    def get_node_weight(self, node_id, model_id):
        weight = self.r.get(self.node_weight % (node_id, model_id))
        return int(weight)

    def get_relation_weight(self, node_from_id, node_to_id, model_id):
        name_from = self.node_rel % (node_from_id, model_id)
        return int(self.r.hget(name_from, node_to_id))

    def get_relations(self, node_id, model_id):
        rels = self.r.hgetall(self.node_rel % (node_id, model_id))
        result = []
        for rel in rels:
            res_el = relation(node_id, rel, rels[rel], model_id)
            result.append(res_el)
        return result

    ################ for difference #####################
    def difference(self, model_id_left, model_id_right):
        left_diff = list(self.r.sdiff(model_id_left, model_id_right))
        right_diff = list(self.r.sdiff(model_id_right, model_id_left))
        return left_diff, right_diff

    def intersection(self, model_id_left, model_id_right):
        intersection = list(self.r.sinter(model_id_left, model_id_right))
        return intersection

    def get_neighbours_ids(self, node_id, left_id):
        q_left = self.node_rel % (node_id, left_id)
        neighs_rel_left = self.r.hgetall(q_left)
        return neighs_rel_left

    ############ for clustering ###########################
    def sum_models(self, id_left, id_right):
        log.info("sum models %s + %s" % (id_left, id_right))
        nodes_right = self.r.smembers(id_right)
        for node_id_right in nodes_right:
            #incrementing weight of node
            weight = self.get_node_weight(node_id_right, id_right)
            self.r.incr(self.node_weight % (node_id_right, id_left), weight)
            #addding relations
            r_neighs_ids = self.r.hgetall(self.node_rel % (node_id_right, id_right))
            for r_neigh_id in r_neighs_ids:
                self.r.hincrby(
                    self.node_rel % (node_id_right, id_left),
                    r_neigh_id,
                    int(r_neighs_ids[r_neigh_id])
                )
                #adding at model
            self.r.sadd(id_left, node_id_right)
            self.r.delete(
                self.node_rel % (node_id_right, id_right),
                self.node_weight % (node_id_right, id_right))

        self.r.delete(id_right)
        return id_left

if __name__ == '__main__':
    import time

    t_start = time.time()

    mh = model_handler(truncate=True)
    model_id = 'test'
    content = [u'привет', u'пока',u'уважь']
    node_id1 = mh.add_node_or_increment(node(content, 10, model_id))

    node = mh.get_node(node_id1, model_id)
    print type(node.content)
    print node.content

    t_stop = time.time()
    print t_stop - t_start