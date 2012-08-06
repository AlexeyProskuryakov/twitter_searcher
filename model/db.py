from bson.son import SON
from pymongo import  *
from pymongo.database import Database
import loggers
from model.tw_model import *
from properties.props import *

__author__ = '4ikist'

log = loggers.logger

users_coll_name = 'users'
relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched_name = 'not_searched'
diffs_name = 'c_diffs'
messages_name = 'messages'
messages_info_name = 'messages_info'


class db_handler():
    def __is_index_presented(self, collection):
        if len(collection.index_information()):
            return True
        return False


    def _db_ignition(self):
        try:
            self.conn = Connection(host, port)
            self.db = Database(self.conn, db_name)

            self.users = self.db[users_coll_name]
            self.entities = self.db[entities_coll_name]
            self.relations = self.db[relations_coll_name]
            self.not_searched = self.db[not_searched_name]
            self.diffs = self.db[diffs_name]
            self.messages = self.db[messages_name]
            self.messages_info = self.db[messages_info_name]

            if not self.__is_index_presented(self.users):
                self.users.create_index('name_', ASCENDING, unique=True)
            if not self.__is_index_presented(self.diffs):
                self.diffs.create_index('date', ASCENDING, unique=False)
            if not self.__is_index_presented(self.messages):
                self.messages.create_index([('time', ASCENDING), ('user', ASCENDING),('message',ASCENDING)], unique=True)


        except Exception as e:
            log.exception(e)
            log.error('error in initialisation of data base connection')
            exit(-1)


    def __init__(self, truncate=False, messages_truncate=False):
        log.info("init db_handler at host: %s, port: %s, db: %s" % (host, port, db_name))
        self._db_ignition()
        if truncate:
            try:
                self.conn.drop_database(db_name)
                self._db_ignition()
            except Exception as e:
                log.exception(e)
                raise e
        if messages_truncate:
            try:
                self.db.drop_collection(messages_info_name)
                self.db.drop_collection(messages_name)
                self._db_ignition()
            except Exception as e:
                log.exception(e)
                raise e




    def save_user(self, ser_user):
        """
        is serialised user from our model user
        """
        log.debug('saving user: %s:%s:%s' % (ser_user['name_'], ser_user['real_name'], ser_user['timeline_count']))
        son = SON(ser_user)
        self.users.save(son)

    def get_user_by_name(self, user_name):
        user = self.users.find_one({'name_':user_name})
        r_user = m_user(user['name_'])
        r_user.serialise_from_db(user)
        return r_user

    def get_user(self, req):
        user = self.users.find_one(req)
        r_user = m_user(user['name_'])
        r_user.serialise_from_db(user)
        return r_user

    def save_diffs(self, ser_diffs):
        """
        saving diffs between one user in difference time
        in two collections - diffs (user_name, date_touch)
        and update users (add to set of diffs_)
        """
        log.debug('saving diffs' % ser_diffs)
        #user for updating
        user = self.users.find_one({'name_': ser_diffs['user_name']})
        son = SON(ser_diffs)
        log.debug(son)
        if user:
            self.users.update({'_id': user['_id']}, {"$addToSet": {'diffs_': son}})
            #todo here if you want to compare two another user_names, name_two is good name date is delete/
            self.diffs.save({'name': ser_diffs['user_name'], 'date': son['date_touch']})

    def get_users_for_diff(self, timedelta=props.timedelta):
        """
        timedelta it is time between now and 'date' of first difference
        """
        users = self.diffs.find({'date': {'$lte': datetime.datetime.now() - timedelta}})
        users = set([user['name'] for user in users])
        self.diffs.remove({'name': {'$in': users}})
        return users

    def get_not_searched_name(self):
       #may be it is not good solve #-,
       not_searched = self.not_searched.find_one()
       if not_searched:
           self.not_searched.remove({'name': not_searched['name']})
           log.debug("loading not searched name: %s" % not_searched['name'])
           return not_searched['name']
       else:
           log.warn('no more users for search :( update collection in db, using scripts.js/create_not_searched()')
           return None

    def verify_user(self, name):
        user = self.users.find_one({'name_': name})
        if user:
            return m_user_status(m_user_status.s_saved)
        return m_user_status(m_user_status.s_none)



    def save_message(self, message):
        self.messages.save(message)

    def save_message_info(self, messages_info):
        self.messages_info.save(messages_info)

if __name__ == '__main__':
    pass
#    db_handler = db_handler(truncate=True)
#
#    db_handler.diffs.save({'name': 'name_1', 'date': datetime.datetime.strptime('2009.12.12_12:12', props.time_format)})
#    db_handler.diffs.save({'name': 'name_2', 'date': datetime.datetime.strptime('2009.12.12_12:13', props.time_format)})
#    db_handler.diffs.save({'name': 'name_3', 'date': datetime.datetime.strptime('2009.12.12_12:14', props.time_format)})
#    db_handler.diffs.save({'name': 'name_4', 'date': datetime.datetime.strptime('2009.12.12_12:15', props.time_format)})
#    db_handler.diffs.save({'name': 'name_5', 'date': datetime.datetime.strptime('2009.12.12_12:16', props.time_format)})
#
#    print db_handler.get_users_for_diff()
#    user = m_user("name")
#    user.real_name = 'test'
#    user.timeline_count = 1000
#
#    db_handler.save_user(user.serialise())
#    time.sleep(5)
#    user = db_handler.get_user({'date_touch':{'$lt':datetime.now()}})
#    print user
