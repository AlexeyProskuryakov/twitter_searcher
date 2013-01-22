from pymongo import ASCENDING
from analysing_data.mc_model import *
import loggers
from model.db import  database
from properties.props import *

log = loggers.logger

__author__ = 'Alesha'

def create_node(dict):
    el = node(dict['content'], dict['weight'], dict['model_id_'])
    el._id = dict['_id']
    return el


def create_relation(dict):
    rel = relation(dict['from_'], dict['to_'], dict['weight'], dict['model_id_'])
    rel._id = dict['_id']
    return rel


class db_mc_handler(database):
    def _schema_init(self):
        self.nodes = self.db['mc_nodes']
        self.relations = self.db['mc_relations']
        self.model_parameters = self.db['mc_parameters']

        if not self._is_index_presented(self.nodes):
            log.info('create nodes index')
            self.nodes.create_index('content', ASCENDING, unique=False)
            self.nodes.create_index('model_id_', ASCENDING, unique=False)

        if not self._is_index_presented(self.relations):
            log.info('create relations index')
            self.relations.create_index([('from_', ASCENDING), ('to_', ASCENDING), ('model_id_', ASCENDING)],
                unique=True)


    def __init__(self, truncate=False):
        database.__init__(self, host_=local_host, port_=local_port, db_name_=local_db_name)
        self._schema_init()

        if truncate:
            self.db.drop_collection(self.nodes)
            self.db.drop_collection(self.relations)
            self.db.drop_collection(self.model_parameters)
            self._schema_init()


    def add_node_or_increment(self, node_element, weight=None):
        if not weight:
            weight = node_element.weight
        saved_el = self.nodes.find_one({'content': node_element.content, 'model_id_': node_element.model_id_})
        if saved_el:
            saved_el['weight'] += weight
            return self.nodes.save(saved_el)
        else:
            return self.nodes.save(node_element.serialise())

    def add_relation_or_increment(self, relation_element, weight=None):
        if not weight:
            weight = relation_element.weight

        saved = self.relations.find_one({'from_': relation_element.from_,
                                         'to_': relation_element.to_,
                                         'model_id_': relation_element.model_id_})
        if saved:
            saved['weight'] += weight
            return self.relations.save(saved)
        else:
            dict = relation_element.serialise()
            return self.relations.save(dict)


    def get_nodes(self, model_id):
        return [create_node(el) for el in self.nodes.find({'model_id_': model_id})]

    def get_node_by_content(self, content, model_id):
        return create_node(self.nodes.find_one({'content': content, 'model_id_': model_id}))

    def get_relations(self, model_id):
        return [create_relation(el) for el in self.relations.find({'model_id_': model_id})]

    def get_relation(self, from_, to_, model_id):
        return create_relation(self.relations.find_one({'from_': from_, 'to_': to_, 'model_id_': model_id}))

    def get_relations_from(self, from_id, model_id):
        rels = self.relations.find({'from_': from_id, 'model_id_': model_id})
        return [create_relation(el) for el in rels]

    def get_relations_to(self, to_id, model_id):
        rels = self.relations.find({'to_': to_id, 'model_id_': model_id})
        return [create_relation(el) for el in rels]

    def get_model_unique_weight(self, model_id):
        return self.nodes.find({'model_id_': model_id}).count()

    def __get_model_weight(self, model_id):
        cur = self.nodes.find({'model_id_': model_id})
        if cur:
            return cur.count()
        else:
            raise Exception('i haven\'t this model id %s' % model_id)


    def __update_node_in_models(self, model_id_more, model_id_less, id):
        """
        adding node (with summing of weight) to model which more
        and removing from model less
        returning id of node in model_id_more
        """

        node_in_model_less = self.nodes.find_one({'_id': id})
        node_in_model_more = self.nodes.find_one({'content': node_in_model_less['content'], 'model_id_': model_id_more})

        if node_in_model_more:
            if node_in_model_less.has_key('old_model_id_'):
                return node_in_model_more['_id']

            node_in_model_more['weight'] += node_in_model_less['weight']
            result_id = self.nodes.save(node_in_model_more)
            self.nodes.update({'_id': node_in_model_less['_id']}, {'$set': {'old_model_id_': model_id_less}})
        else:
            self.nodes.update({'_id': node_in_model_less['_id']},
                {'$set': {'model_id_': model_id_more, 'old_model_id_': model_id_less}})
            result_id = node_in_model_less['_id']

        return result_id

    def sum_models(self, model_id_left, model_id_right):
        """
        note input ids must be
        create sum of model when model with more elements is devour model with less elements
        after this all elements which was in absorbed model have old_model_id_ field which identify belonging that
        element to old model/

        returning model id of model with more elements with new stateless
        """
        try:
            left_weight = self.__get_model_weight(model_id_left)
            right_weight = self.__get_model_weight(model_id_right)
        except Exception as e:
            log.exception(e)
            log.error("may be you must save models previosly or error in their model_id_?")
            return None

        if left_weight >= right_weight:
            more_model_id = model_id_left
            less_model_id = model_id_right
        else:
            more_model_id = model_id_right
            less_model_id = model_id_left

        #update nodes to new model_id_
        #for any relation in less model:
        for rel_less in self.relations.find({'model_id_': less_model_id}):
            #flushing nodes and updating
            from_ = rel_less['from_']
            new_from_id = self.__update_node_in_models(more_model_id, less_model_id, from_)
            to_ = rel_less['to_']
            new_to_id = self.__update_node_in_models(more_model_id, less_model_id, to_)
            #process relation
            new_old_relation = relation(new_from_id, new_to_id, rel_less['weight'], model_id_=more_model_id)
            if rel_less.has_key('additional_obj'):
                new_old_relation.additional_obj = rel_less['additional_obj']

            self.add_relation_or_increment(new_old_relation)
            self.relations.update({'_id': rel_less['_id']}, {'$set': {'old_model_id_': rel_less['model_id_']}})

        self.model_parameters.update({'model_id_': more_model_id}, {'$push': {'include': less_model_id}})
        return more_model_id

