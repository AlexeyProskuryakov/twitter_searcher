"""
visualisation of users graph

"""

import json
import urllib2
import loggers

from model import tw_model
from model.db import db_handler
from model.tw_model import m_user
from properties import props

log = loggers.logger

all_node_names = list()

data_buff = []
buff_size = 100

def send(data):
    try:
        log.debug(data)
        jdata = json.dumps(data)
        c = urllib2.urlopen(props.v_host, jdata)
        log.info(c.read())
    except Exception as e:
        log.error('sending error')
        log.exception(e)


def add_nodes(nodes):
    nodes_add_cmd = {'an': nodes}
    send(nodes_add_cmd)


def add_edges(edges):
    edges = {'ae': edges}
    send(edges)


def form_graph(m_user, user_weight = 10, edge_weights=None, edge_colors=None):
    if not edge_weights:
        edge_weights = {tw_model.followers: 10, tw_model.friends: 10, tw_model.mentions: 10}
    if not edge_colors:
        edge_colors = {tw_model.followers: (1, 1, 1), tw_model.friends: (2, 2, 2), tw_model.mentions: (3, 3, 3)}

    relations = m_user.get_relations()
    edges = {}
    nodes = {m_user.name_: {'label': m_user.name_, 'weight': user_weight}}


    def form_edges_nodes(rel_type, nodes, edges):
        target_users = relations[rel_type]
        color = edge_colors[rel_type]
        weight = edge_weights[rel_type]

        for target in  target_users:
            edges = dict(edges, **{
                str(target) + str(m_user.name_): {'source': m_user.name_, 'target': target, 'weight': weight,
                                                    'directed': True, 'r': color[0], 'g': color[1], 'b': color[2]}})
            nodes = dict(nodes, **{target: {'label': target, 'weight': user_weight}})

        return nodes, edges

    nodes,edges = form_edges_nodes(tw_model.friends,nodes,edges)
    nodes,edges = form_edges_nodes(tw_model.followers,nodes,edges)
    nodes,edges = form_edges_nodes(tw_model.mentions,nodes,edges)

    return nodes,edges

def visualise_users():
    db = db_handler()
    users = db.users.find()
    for user in users:
        user = m_user.create(user)
        print user.name_
        nodes,edges = form_graph(user)
        add_nodes(nodes)
        add_edges(edges)

if __name__ == '__main__':
    visualise_users()
    