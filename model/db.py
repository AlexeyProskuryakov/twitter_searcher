from pymongo import  *

__author__ = '4ikist'

port = 27017
host = 'localhost'
db_name = 'ttr'
coll_name = 'users'

class db_handler():
    def __init__(self):
        conn = Connection(host, port)
        db = conn[db_name]
        self.users = db[coll_name]

    def save_user(self, ser_user):
        print 'saving user: ', ser_user
        self.users.save(ser_user)

    def form_nodes(self, f_name, parameter_f=lambda x: len(x['tweets_count'])):
        file = open(f_name, 'w+')
        file.write("Label,Id;Weight;\n")
        f_users = self.users.find()
        for user in f_users:
            file.write(user['name'] + ";" + user['name'] + ";" + parameter_f(user) + "\n")
        file.close()

    def get_out_from(self, user):
        return user['friends']

    def get_in_to(self, user):
        return user['followers']

    def form_edges(self, f_name):
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;\n")
        relations = set()
        for user in self.users.find():
            for out_ in self.get_out_from(user):
                term = (user['name'], out_)
                relations.add(term)
            for in_ in self.get_in_to(user):
                term = (in_, user['name'])
                relations.add(term)
        for relation in relations:
            file.write(relation[0] + ";" + relation[1] + ";;")
        file.close()