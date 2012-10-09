from visualise.vis_machine import add_edges, add_nodes

__author__ = '4ikist'

class mc_vis():
    @staticmethod
    def put_mc_nodes(nodes):
        g_nodes = {}
        for node in nodes:
            id = str(node._id)
            label = node.content
            node = {id: {'label': label, 'size': node.weight * 10}}
            g_nodes = dict(g_nodes, **node)
        add_nodes(g_nodes)

    @staticmethod
    def put_mc_relations(relations):
        g_rels = {}
        for relation in relations:
            id = str(relation._id)
            source = str(relation.from_)
            target = str(relation.to_)
            edge = {id: {'source': source, 'target': target, 'weight': relation.weight * 10, 'directed': True}}
            g_rels = dict(g_rels, **edge)
        add_edges(g_rels)

  