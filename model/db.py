from bson import BSON
from bson.son import SON
from pymongo import  *
from pymongo.collection import Collection
from pymongo.database import Database
import time
import loggers
from model.tw_model import *
from properties.props import *

__author__ = '4ikist'

log = loggers.logger

users_coll_name = 'users'
relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched = 'not_searched'
diffs = 'diffs'

#todo create versions for user in version - dbref into diff.
#todo create method for ensuring indexes!
#todo create serialisation users

class db_handler():

    def __is_index_presented(self, collection_name,db):
        c = Collection(db,collection_name)
        log.debug("index info: %s"% c.index_information())
        

    def _db_ignition(self):
        self.conn = Connection(host, port)
        self.db = Database(self.conn, db_name)

        self.users = self.db[users_coll_name]
        self.entities = self.db[entities_coll_name]
        self.relations = self.db[relations_coll_name]
        self.not_searched = self.db[not_searched]
        self.diffs = self.db[diffs]

        self.__is_index_presented(users_coll_name,self.db)

    def ensure_indexes(self):
        pass

    def __init__(self,truncate = False):
        log.info("init db_handler at host: %s, port: %s, db: %s"%(host,port,db_name))
        self._db_ignition()
        if truncate:
            try:
                self.conn.drop_database(db_name)
                self._db_ignition()
            except Exception as e:
                log.exception(e)
                raise e



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
        son = SON(ser_user)
        self.users.save(son)

    def get_user_by_name(self, user_name):
        return self.users.find_one({'name': user_name})

    def save_diffs(self, ser_diffs):
        log.debug( 'saving diffs'% ser_diffs)
        user = self.users.find_one({'name': ser_diffs['name']})
        if user:
            id = self.diffs.save(ser_diffs)
            log.info('save diff with id %s'%id)
            self.users.update({'_id':user['_id']},{"$addToSet":{'diffs':id}})

    def get_users_for_diff(self,timedelta):
        pass

    def verify_user(self,name):
        user = self.users.find_one({'name':name})
        if user:
            return m_user_status(m_user_status.s_saved)
        return m_user_status(m_user_status.s_none)

    def get_user(self, req):
        user = self.users.find_one(req)
        return user

if __name__ == '__main__':
    pass
#    db_handler = db_handler(truncate=True)
#    user = m_user("name")
#    user.real_name = 'test'
#    user.timeline_count = 1000
#
#    db_handler.save_user(user.serialise())
#    time.sleep(5)
#    user = db_handler.get_user({'date_touch':{'$lt':datetime.now()}})
#    print user
