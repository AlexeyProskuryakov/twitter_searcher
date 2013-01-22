import networkx as nx
import matplotlib.pyplot as plt

__author__ = '4ikist'

def draw_graph(model, color=None):
    if not color: color = {'node': 'r', 'edge': 'b'}
    g = nx.DiGraph()

    labels = {}
    for node in model.get_nodes():
        g.add_node(node._id, {'label': node.content, 'weight': node.weight})
        label = r''.join(node.content)+'$'
        print label
        labels[node._id] = label

    for edge in model.get_relations():
        g.add_edge(edge.from_, edge.to_, {'weight': edge.weight})

    pos = nx.graphviz_layout(g)
    nx.draw_networkx_nodes(g, pos, nodecolor=color['node'])
    nx.draw_networkx_labels(g, pos, labels)
    nx.draw_networkx_edges(g, pos)

    plt.show()

if __name__ == '__main__':
    pass
