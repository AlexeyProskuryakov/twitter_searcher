from differences.d_model import difference_element,m_hash_dict
from markov_chain_machine import markov_chain,element

__author__ = 'Alesha'
__doc__ = """
markov chain difference logic implementing
"""


#todo realise
def compile_chain(markov_chain_):
    """
    executings for calculations frequency of markov chain/
    """
    for word in markov_chain_.words:
        word.f_weight = float(word.weight)/markov_chain_.words_count_
        word.f_rel_weight = float(sum([relation.weight for relation in markov_chain_._get_all_relations(word.mc_id)]))/float(sum([relation.weight for relation in markov_chain_._get_all_relations()]))

    for relation in markov_chain_.relations:
        relation.f_weight = float()


def diff_markov_chains(i_markov_chain,i_markov_chain_2):
    """
    for using into difference machine processing like
    difference_factory.add_i_function(diff_markov_chains)
    """
    diff_element = difference_element('mc_difference',None)

    nodes_left = set(i_markov_chain.words)
    nodes_right = set(i_markov_chain_2.words)

    intersection_nodes = nodes_left.intersection(nodes_right)
    symmetric_difference = nodes_left.symmetric_difference(nodes_right)

    edges_left = set(i_markov_chain.references)
    edges_right = set(i_markov_chain_2.references)

    intersection_edges = edges_left.intersection(edges_right)
    symmetric_difference = edges_left.symmetric_difference(edges_right)

    #tolerance

    #at first you must create markov chain at intersection nodes and edges
    markov_chain._create(intersection_nodes,intersection_edges)
    for intersection_node in intersection_nodes:
        relations_left_node = i_markov_chain.get_relations(intersection_node.content)
        relations_left_node.extend( i_markov_chain.get_relations(intersection_node.content,is_from = 1))

        relations_left_node = set(relations_left_node)


        relations_right_node = i_markov_chain_2.get_relations(intersection_node.content)
        relations_right_node.extend(  i_markov_chain_2.get_relations(intersection_node.content,is_from = 1))

        relations_right_node = set(relations_right_node)

        intersection_relations = relations_right_node.intersection(relations_right_node)
        symmetric_difference_relations = relations_right_node.symmetric_difference(relations_left_node)






