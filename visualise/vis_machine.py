"""
visualisation of users graph

"""
from datetime import datetime
import json
from time import sleep
import urllib2
import time
import loggers
from model import tw_model
from model.db import db_handler
from model.tw_model import m_user
from properties import props

log = loggers.logger

all_node_names = list()


def send(data):
    try:
        jdata = json.dumps(data)
        log.debug(jdata)
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


def form_graph(m_user, db):
    relations = m_user.get_relations()
    edges = {}
    nodes = {m_user.name_:{'label':m_user.name_, 'weight': 10}}

    #followers
    for follower in relations[tw_model.followers]:
        if db.users.find_one({'name_':follower}):
            edges = dict(edges, **{str(follower) + str(m_user.name_):{'source': m_user.name_, 'target': follower, 'weight': 5,'directed':True,'r':1.0, 'g':0.5, 'b':0.5}})
            nodes = dict(nodes,**{follower:{'label':follower, 'weight': 10}})
        else:
            edges = dict(edges, **{str(follower) + str(m_user.name_):{'source': m_user.name_, 'target': follower, 'weight': 1,'directed':True,'r':1.0, 'g':0.5, 'b':0.5}})
            nodes = dict(nodes,**{follower:{'label':follower, 'weight': 2}})

    #friends
    for friend in relations[tw_model.friends]:
        if db.users.find_one({'name_':friend}):
            edges = dict(edges, **{str(friend) + str(m_user.name_):{'target': m_user.name_, 'source': friend, 'weight': 5,'directed':True,'r':0.5, 'g':1.0, 'b':0.5}})
            nodes = dict(nodes,**{friend:{'label':friend, 'weight': 10}})
        else:
            edges = dict(edges, **{str(friend) + str(m_user.name_):{'target': m_user.name_, 'source': friend, 'weight': 1,'directed':True,'r':0.5, 'g':1.0, 'b':0.5}})
            nodes = dict(nodes,**{friend:{'label':friend, 'weight': 2}})

    #mentions
    for ment in relations[tw_model.mentions]:
        if db.users.find_one({'name_':ment}):
            edges = dict(edges, **{str(ment) + str(m_user.name_):{'source': m_user.name_, 'target': ment, 'weight': 10,'directed':True,'r':0.5, 'g':0.5, 'b':1.0}})
            nodes = dict(nodes,**{ment:{'label':ment, 'weight': 10}})
        else:
            edges = dict(edges, **{str(ment) + str(m_user.name_):{'source': m_user.name_, 'target': ment, 'weight': 5,'directed':True,'r':0.5, 'g':0.5, 'b':1.0}})
            nodes = dict(nodes,**{ment:{'label':ment, 'weight': 2}})

    return edges, nodes


def process():
    db = db_handler()
    users = db.users.find()
    for user in users:
        user = m_user.create(user)
        print user.name_
        edges, nodes = form_graph(user,db)
        add_nodes(nodes)
        add_edges(edges)

if __name__ == '__main__':
    for i in range(365):
        time_start = datetime.now()
        process()
        time_stop = datetime.now()
        timedelta = time_stop.hour - time_start.hour
        sleep(1*60*60*24 - timedelta*60*60)

    