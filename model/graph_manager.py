from model.db import db_handler
from properties import props

__author__ = 'Alesha'
class db_graph(db_handler):
    def __init__(self):
        self.handler = db_handler.__init__(props.host,props.port)

    def form_nodes(self, f_name, parameter_f=lambda x: x['tweets_count']):
        file = open(f_name, 'w+')
        file.write("Label;Id;Weight;\n")
        f_users = self.handler.users.find()
        for user in f_users:
            file.write(user['name'] + ";" + user['name'] + ";" + str(parameter_f(user)) + "\n")
        file.close()
        print 'nodes formed'


    def form_edges(self, f_name):
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;\n")
        relations = set()
        for user in self.handler.users.find():
            for out_ in user['friends']:
                term = (user['name'], out_)
                relations.add(term)
            for in_ in user['followers']:
                term = (in_, user['name'])
                relations.add(term)
        for relation in relations:
            file.write(relation[0] + ";" + relation[1] + ";;\n")
        print 'edges formed'
        file.close()

    #todo
    def form_entities_edges(self, f_name):
        entities = self.handler.entities.find()
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;\n")

