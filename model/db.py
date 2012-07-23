from pymongo import  *
from pymongo.database import Database
import loggers
from properties.props import *

__author__ = '4ikist'

log = loggers.logger

users_coll_name = 'users'
relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched = 'not_searched'
diffs = 'diffs'
#todo create versions for user in version - dbref into diff.
class db_handler():
    def __init__(self):
        log.info("init db_handler at host: %s, port: %s, db: %s"%(host,port,db_name))
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
        if not_searched:
            self.not_searched.remove({'name': not_searched['name']})
            log.debug("loading not searched name: %s"%not_searched['name'])
            return not_searched['name']
        else:
            log.warn('no more users for search :( update collection in db, using scripts.js/create_not_searched()')
            return None

    def save_user(self, ser_user):
        log.debug( 'saving user: %s:%s:%s'% (ser_user['name'],ser_user['real_name'],ser_user['timeline_count']))
        self.users.save(ser_user)

    def get_user_by_name(self, user_name):
        return self.users.find_one({'name': user_name})

    def save_diffs(self, ser_diffs):
        log.debug( 'saving diffs'% ser_diffs)
        user = self.users.find_one({'name': ser_diffs['name']})
        if user:
            id = self.diffs.save(ser_diffs)
            log.info('save diff with id %s'%id)
            self.users.update({'_id':user['_id']},{"$addToSet":{'diffs':id}})



if __name__ == '__main__':
    pass