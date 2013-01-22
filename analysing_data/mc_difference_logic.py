# coding=utf-8
import math
import numpy as np
from analysing_data.redis_handlers import model_handler
import loggers
from markov_chain_machine import markov_chain
from networkx.algorithms import centrality
import networkx as nx

log = loggers.logger

def create_graph(nodes, model):
    g = nx.DiGraph()
    for node in nodes:
        g.add_node(node._id, {'content': node.content, 'weight': node.weight})
        neigh = [el for el in model.get_node_neigh(node._id) if el in nodes]
        rels = [model.get_relation(node._id, el._id) for el in neigh]
        for rel in rels:
            if rel:
                g.add_edge(rel.from_, rel.to_, {'weight': rel.weight})
    return g


def calc_defence(diff_ids, int_ids, model_id, model_w, model_handler):
    defence = 0
    tolerance = 0
    for diff_id in diff_ids:
        neighs = model_handler.get_neighbours_ids(diff_id, model_id)
        neighs_list = list(neighs)
        neighs_in_int = np.intersect1d(neighs_list, int_ids, True)

        w_diff = model_handler.get_node_weight(diff_id, model_id)

        if len(neighs_in_int):
            neighs_in_diff = np.intersect1d(neighs_list, diff_ids)

            sum_rel_diff = sum([model_handler.get_relation_weight(diff_id, i, model_id) for i in neighs_in_diff])
            sum_rel_int = sum([model_handler.get_relation_weight(diff_id, i, model_id) for i in neighs_in_int])
            if sum_rel_diff == 0:
                sum_rel_diff = 1
            if sum_rel_int == 0:
                sum_rel_int = 1

            for neigh in neighs:
                w_neigh = model_handler.get_node_weight(neigh, model_id)
                w_r_neigh = model_handler.get_relation_weight(neigh, diff_id, model_id)

                if neigh in neighs_in_int:
                    ch = float(math.fabs(float(w_neigh - w_diff)) * w_r_neigh)
                    tolerance += ch / sum_rel_diff
                else:
                    ch = (float(w_neigh) + w_diff) * w_r_neigh
                    defence += ch / sum_rel_int

        else:
            defence += float(w_diff) / model_w
    return tolerance, defence


def get_centrality(def_centrality, toll_centrality, model, nodes_int):
    left_b_centr = centrality.betweenness_centrality(model.get_nx_graph())
    left_c_centr = centrality.closeness_centrality(model.get_nx_graph())
    for el in left_b_centr:
        node = model.get_node_by_id(el)
        if node in nodes_int:
            toll_centrality += left_c_centr[el] + left_b_centr[el]
        else:
            def_centrality += left_c_centr[el] + left_b_centr[el]
    return def_centrality, toll_centrality


def diff_markov_chains(model_left_id, model_right_id, model_handler):
    #log.info("start diff %s <-> %s" % (model_left_id, model_right_id))

    left_w = model_handler.get_weight(model_left_id)
    right_w = model_handler.get_weight(model_right_id)

    int_ids = model_handler.intersection(model_left_id, model_right_id)
    diff_left_ids, diff_right_ids = model_handler.difference(model_left_id, model_right_id)

    tolerance = 0
    model_w = math.fabs(float(left_w) - right_w) if left_w != right_w else float(left_w) / 2
    for int_id in int_ids:
        w_left_node = model_handler.get_node_weight(int_id, model_left_id)
        w_right_node = model_handler.get_node_weight(int_id, model_right_id)
        #some calculating for EL
        el = float(w_left_node + w_right_node) / model_w


#        neighs_left = model_handler.get_neighbours_ids(int_id, model_left_id)
#        neighs_right = model_handler.get_neighbours_ids(int_id, model_right_id)
#        neighs_left_keys = neighs_left.keys()
#        neighs_right_keys = neighs_right.keys()
#
#        sim_neighs = np.intersect1d(neighs_left_keys, neighs_right_keys, True)
#        int_neighs_left = np.intersect1d(neighs_left_keys, int_ids, True)
#        int_neighs_right = np.intersect1d(neighs_right_keys, int_ids, True)
#
#        dif_neighs_left = np.intersect1d(neighs_left_keys, diff_left_ids, True)
#        dif_neighs_right = np.intersect1d(neighs_right_keys, diff_right_ids, True)
#
#        #some calculating for K_rel
#
#        w_left_i = sum([float(neighs_left[i]) for i in int_neighs_left])
#        w_left_d = sum([float(neighs_left[i]) for i in dif_neighs_left])
#        w_left_s = sum([float(neighs_left[i]) for i in sim_neighs])
#
#        if w_left_d == 0:
#            w_left_d = 1
#
#        w_el = float(w_left_i + w_left_s) / w_left_d
#
#        w_right_i = sum([float(neighs_right[i]) for i in int_neighs_right])
#        w_right_d = sum([float(neighs_right[i]) for i in dif_neighs_right])
#        w_right_s = sum([float(neighs_right[i]) for i in sim_neighs])
#
#        if w_right_d == 0:
#            w_right_d = 1
#        w_el += float(w_right_i + w_right_s) / w_right_d
#
#        el *= w_el
        tolerance += el

    defence_l, n_tol_l = calc_defence(diff_left_ids, int_ids, model_left_id, left_w, model_handler)
    defence_r, n_tol_r = calc_defence(diff_right_ids, int_ids, model_right_id, right_w, model_handler)
    defence = defence_l + defence_r
    tolerance += n_tol_l + n_tol_r

    return tolerance - defence

if __name__ == '__main__':
    handler = model_handler(truncate=True)

    mc1 = markov_chain('left_test', handler, n_of_gram_=1)
    mc1.add_message([u'ф', 'd3', 'd2'])
    mc1.add_message(['i1', 'd3', 'i2'])
    mc1.add_message(['i1', 'i4'])
    mc1.add_message(['i1', 'i2', 'i3'])

    mc1.print_me()

    mc2 = markov_chain('right_test', handler, n_of_gram_=1)

    mc2.add_message(['d2_', 'd1_', 'd3_'])
    mc2.add_message(['i2', 'i1', 'i3', 'i2'])
    mc2.add_message(['i1', 'i3', 'i4'])
    mc2.add_message(['d1_', 'i3', 'i4', 'd1_'])

    mc2.print_me()

    result = diff_markov_chains(mc1.model_id_, mc2.model_id_, handler)
    handler.sum_models(mc1.model_id_, mc2.model_id_)
    print '\n\n\n---------------------sum:'
    mc1.print_me()


#    model_new_id = booster.sum_models('right_test', 'left_test')
#    new_mc = markov_chain(model_new_id, booster)
#
#    new_mc.print_me()

#    print centrality.betweenness_centrality(mc1.get_nx_graph(), normalized=True)
#    print centrality.closeness_centrality(mc1.get_nx_graph(), normalized=True)
#print


