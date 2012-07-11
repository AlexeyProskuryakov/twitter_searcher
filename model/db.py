from pymongo import  *
<<<<<<< HEAD
from pymongo.database import Database
=======
>>>>>>> 81b58d9bc1cf3b543044289988a56ed0e819ee41

__author__ = '4ikist'

port = 27017
<<<<<<< HEAD
host = '178.49.120.77'
db_name = 'ttr'
users_coll_name = 'users'
relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched = 'not_searched'
class db_handler():
    def __init__(self):
        self.conn = Connection(host, port)
        self.db = Database(self.conn, db_named)
        self.users = self.db[users_coll_name]

        self.entities = self.db[entities_coll_name]
        self.relations = self.db[relations_coll_name]
        self.not_searched = self.db[not_searched]

    def get_not_searched(self):
        return self.not_searched.find_one()
=======
host = 'localhost'
db_name = 'ttr'
coll_name = 'users'

class db_handler():
    def __init__(self):
        conn = Connection(host, port)
        db = conn[db_name]
        self.users = db[coll_name]
>>>>>>> 81b58d9bc1cf3b543044289988a56ed0e819ee41

    def save_user(self, ser_user):
        print 'saving user: ', ser_user
        self.users.save(ser_user)

<<<<<<< HEAD
    def form_nodes(self, f_name, parameter_f=lambda x: x['tweets_count']):
        file = open(f_name, 'w+')
        file.write("Label;Id;Weight;\n")
        f_users = self.users.find()
        for user in f_users:
            file.write(user['name'] + ";" + user['name'] + ";" + str(parameter_f(user)) + "\n")
        file.close()
        print 'nodes formed'
=======
    def form_nodes(self, f_name, parameter_f=lambda x: len(x['tweets_count'])):
        file = open(f_name, 'w+')
        file.write("Label,Id;Weight;\n")
        f_users = self.users.find()
        for user in f_users:
            file.write(user['name'] + ";" + user['name'] + ";" + parameter_f(user) + "\n")
        file.close()
>>>>>>> 81b58d9bc1cf3b543044289988a56ed0e819ee41

    def get_out_from(self, user):
        return user['friends']

    def get_in_to(self, user):
        return user['followers']

    def form_edges(self, f_name):
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;\n")
        relations = set()
        for user in self.users.find():
<<<<<<< HEAD
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
        entities = self.entities.find()
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;\n")


if __name__ == '__main__':
    db_handler = db_handler()
    db_handler.form_edges("d:/temp/edges.csv")
    db_handler.form_nodes("d:/temp/nodes.csv")
=======
            for out_ in self.get_out_from(user):
                term = (user['name'], out_)
                relations.add(term)
            for in_ in self.get_in_to(user):
                term = (in_, user['name'])
                relations.add(term)
        for relation in relations:
            file.write(relation[0] + ";" + relation[1] + ";;")
        file.close()
>>>>>>> 81b58d9bc1cf3b543044289988a56ed0e819ee41
