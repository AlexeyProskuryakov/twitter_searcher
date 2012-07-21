from pymongo import  *
from pymongo.database import Database

__author__ = '4ikist'

#todo go out in properties!
port = 27017
#host = '178.49.120.77'
host = '127.0.0.1'

db_name = 'ttr'
users_coll_name = 'users'
relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched = 'not_searched'
diffs = 'diffs'

class db_handler():
    def __init__(self):
        self.conn = Connection(host, port)
        self.db = Database(self.conn, db_name)

        self.users = self.db[users_coll_name]
        self.entities = self.db[entities_coll_name]
        self.relations = self.db[relations_coll_name]
        self.not_searched = self.db[not_searched]
        self.diffs = self.db[diffs]

    def get_not_searched_name(self):
        #may be it is not good solve #-,
        not_searched = self.not_searched.find_one()
        self.not_searched.remove({'name': not_searched['name']})
        return not_searched['name']

    def save_user(self, ser_user):
        print 'saving user: ', ser_user
        self.users.save(ser_user)

    def get_user_by_name(self, user_name):
        return self.users.find_one({'name': user_name})

    def save_diffs(self, ser_diffs):
        print 'saving diffs', ser_diffs
        if self.users.find(
                {'$or':
                     [{'name': ser_diffs['one_name']},
                             {'name': ser_diffs['two_name']}
                     ]}).count() > 0:
            self.diffs.save(ser_diffs)


if __name__ == '__main__':
    pass