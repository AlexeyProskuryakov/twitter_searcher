from bson.son import SON
from pymongo import  *
from pymongo.database import Database
import loggers
from model.tw_model import *
from properties import props
from properties.props import *

__author__ = '4ikist'

log = loggers.logger


#################
#collections names
#################
users_coll_name = 'users'

relations_coll_name = 'relations'
entities_coll_name = 'entities'
not_searched_name = 'not_searched'

users_for_update_name = 'm_users'

diffs_output_name = 'diffs_users_output'

#fields are initted in diff machine
diffs_input_name = 'diffs_users_input'
diffs_input_fields = ['name_','date_touch_']

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

            self.diffs_input = self.db[diffs_input_name]
            self.diffs_output = self.db[diffs_output_name]

            self.messages = self.db[messages_name]
            self.messages_info = self.db[messages_info_name]

            if not self.__is_index_presented(self.users):
                self.users.create_index('name_', ASCENDING, unique=True)
            if not self.__is_index_presented(self.diffs_input):
                self.diffs_input.create_index('date_touch_', ASCENDING, unique=False)
                self.diffs_input.create_index('user_name', ASCENDING, unique=True)
            if not self.__is_index_presented(self.diffs_output):
                self.diffs_output.create_index('date_touch_',ASCENDING,unique=False)
            if not self.__is_index_presented(self.messages):
                self.messages.create_index([('time', ASCENDING), ('user', ASCENDING),('message',ASCENDING)], unique=True)

            self.db.eval(code='db.loadServerScripts();')

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
        return m_user.create(user)

    def get_user(self, req):
        user = self.users.find_one(req)
        return m_user.create(user)

    def save_diffs(self, ser_diffs):
        """
        saving diffs between one user in difference time
        in two collections - diffs (user_name, date_touch)
        and update users (add to set of diffs_)

        """
        log.debug('saving diffs' % ser_diffs)
        #user for updating
        user = self.users.find_one({'name_': ser_diffs['user_name']})
        if user:
            son = SON(ser_diffs)
            log.debug(son)
            self.users.update({'_id': user['_id']}, {"$addToSet": {'diffs_': {'id':ser_diffs['diff_id'],'datetime':datetime.datetime.now()}}})
            self.users.update({'_id':user['_id']},{"$set":{'date_touch_':datetime.datetime.now()}})
            self.diffs_output.save(son)
        else:
            log.warn('user for this diff not found...')

    def get_users_for_diff(self,use_input_diff_collection = False,limit = 10):
        """
        if use_input_diff_collection - getting from collection diff_users_input user names with limit
        else get from collection users users names which date_touch_ between:
            now - props.timdelta and now
            or
            props.time_start and props.time_stop
        """
        users = []
        if use_input_diff_collection:
            diffs = self.diffs_input.find(limit=limit)
            for diff in diffs:
                self.diffs_input.remove(diff)
                user = m_user.create(self.users.find_one({'name_':diff['name_']}))
                users.append(user)
            return users
        else:
            user_objects = []
            if props.timedelta:
                user_objects = self.users.find(
                        {'date_touch_':{'$lt':datetime.datetime.now() - props.timedelta}},
                                                                                        limit= limit)
            elif props.time_start and props.time_stop:
                user_objects = self.users.find({'$and':[
                        {'date_touch_':{'$gte':props.time_start}},
                        {'date_touch_':{'$lte':props.time_stop}}
                ]},limit = limit)

            users = [m_user.create(user) for user in user_objects]
            return users

    def verify_user(self, name):
        user = self.users.find_one({'name_': name})
        if user:
            if user['date_touch_']+props.min_timedelta > datetime.datetime.now():
                return m_user_status(m_user_status.s_updated)
            return m_user_status(m_user_status.s_update_needed)
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
