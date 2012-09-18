from differences.d_model import difference_element, m_hash_dict
import loggers
from markov_chain_machine import markov_chain, element

__author__ = 'Alesha'
__doc__ = """
markov chain difference logic implementing
"""
log = loggers.logger

#todo realise
def compile_chain(markov_chain_):
    """
    executings for calculations frequency of markov chain/
    """
    for word in markov_chain_.words:
        word.f_weight = float(word.weight) / markov_chain_.words_count_
        word.f_rel_weight = float(
            sum([relation.weight for relation in markov_chain_.get_all_relations(id=word.mc_id)])) / float(
            markov_chain_.relations_count_)

    for relation in markov_chain_.relations:
        relation.f_weight = float(sum)


def get_messages(markov_chain_id, difference_set, start_id=0, relations=None, depth=0):
    pass


def get_paths_in(markov_chain, difference_set, start_id=0, relations=None, depth=0):
    """
    returning material for compiling paths
    this is dictionary of {depth of relation:relations list}
    """
    #from start
    if not relations: relations = []

    start_edge_out_relations = markov_chain._get_relations_by_id(start_id)
    all_from = len(start_edge_out_relations)

    depth_relations = []
    from_node = markov_chain.words[start_id]
    for relation in start_edge_out_relations:
        to_node = markov_chain.words[relation.content[1]]
        if to_node in difference_set:
            relation.additional_object = {'node_weight_in': to_node.weight}
            depth_relations.append(relation)

    relations.append({'relations': depth_relations, 'count_adjacent': all_from, 'depth': depth, 'from_node': from_node})

    #by intersection work with any element recursive
    intersection = difference_set.intersection(to_nodes)
    for int_el in intersection:
        #mutate relations
        get_paths_in(markov_chain, difference_set, start_id=int_el.mc_id, relations=relations)

    return relations


def compile_relations(relations, hash=lambda one_rel, many_rel: one_rel.weigh / many_rel['count_adjacent']):
    for relation in relations:
        pass


def EL(node, node2, size):
    """
    now it use content. in owerriding it maybe more another
    """
    pass


def KrL(rel_1, rel_2, mc_1, mc_2):
    pass


def KnL(node1, node2, mc_1, mc_2, KrL=KrL):
    pass


def mc_size(mc1, mc2):
    #unique and non unique
    pass


def sum_of_tolerance(tolerance_old, tolerance_new):
    return tolerance_new + tolerance_old


def diff_markov_chains(_markov_chain_left, _markov_chain_right, EL=EL, KnL=KnL, Krl=Krl, size=mc_size,
                       sum_of_tolerance_f=sum_of_tolerance,adj_index = adj_index):
    """
    for using into difference machine processing like
    difference_factory.add_i_function(diff_markov_chains)

    difference two mc:
    1) tolerance = by_intersection:( any_node in intersection EL of weights in input chains / their sizes + their siblings at 1..n
    which equals KnL = difference and intersection between their relations and nodes at another models / their sizes)
    + paths of intersection
    2) defence = by_differences:(any node in ... his weight / their sizes + their siblings at 1..n which equals Knl ... )
    """
    diff_element = difference_element('mc_difference', None)

    nodes_left = set(_markov_chain_left.words)
    nodes_right = set(_markov_chain_right.words)

    l_intersection_nodes = list(nodes_left.intersection(nodes_right))
    r_intersection_nodes = list(nodes_right.intersection(nodes_left))

    l_difference = nodes_left.difference(nodes_right)
    r_difference = nodes_right.difference(nodes_left)

    #tolerance

    tolerance = 0

    for int_id in range(len(l_intersection_nodes)):
        r_int_node = r_intersection_nodes[int_id]
        l_int_node = l_intersection_nodes[int_id]
        el_node = EL(r_int_node, l_int_node, size)

        knl_node = KnL(r_int_node, l_int_node, _markov_chain_left, _markov_chain_right, Krl)
        tolerance_el = el_node * knl_node
        tolerance = sum_of_tolerance_f(tolerance, tolerance_el)

    defence = 0
    for l_diff_el in l_difference:
        defence +=l_diff_el.weight
        adj_elements = _markov_chain_left._get_adjacent_elements(l_diff_el, adj_ind=adj_index)
        true_defence = sum([el.weight for el in adj_elements.difference(l_intersection_nodes)])
        false_defence = adj_elements.intersection(r_intersection_nodes)

        










