from bson.son import SON
from pymongo import  *
from pymongo.database import Database
import loggers
from model.tw_model import *
from properties import props
from properties.props import *
import tools

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
diffs_input_fields = ['name_', 'date_touch_']

messages_name = 'messages'
messages_info_name = 'messages_info'

users_not_loaded_name = 'users_not_loaded'

class database():
    def __init__(self, host_, port_, db_name_):
        try:
            log.info("connect to db at host: %s port: %s db_name: %s" % (host_, port_, db_name_))
            self.conn = Connection(host_, port_)
            self.db = Database(self.conn, db_name_)
        except Exception as e:
            log.exception(e)
            log.error('error in initialisation of data base connection')
            exit(-1)

    def _is_index_presented(self, collection):
        if len(collection.index_information()):
            return True
        return False


class db_handler(database):
    def _main_schema_ignition(self):
        self.users = self.db[users_coll_name]
        self.entities = self.db[entities_coll_name]
        self.relations = self.db[relations_coll_name]

        self.diffs_input = self.db[diffs_input_name]
        self.diffs_output = self.db[diffs_output_name]

        self.messages = self.db[messages_name]
        self.messages_info = self.db[messages_info_name]

        self.users_not_loaded = self.db[users_not_loaded_name]
        if not self._is_index_presented(self.users):
            log.info("creating index for users")
            self.users.create_index('name_', ASCENDING, unique=True)
        if not self._is_index_presented(self.diffs_input):
            log.info("creating index for diffs_input")
            self.diffs_input.create_index('date_touch_', ASCENDING, unique=False)
            self.diffs_input.create_index('user_name', ASCENDING, unique=True)
        if not self._is_index_presented(self.diffs_output):
            log.info("creating index for diffs_output")
            self.diffs_output.create_index('date_touch_', ASCENDING, unique=False)
        if not self._is_index_presented(self.messages):
            log.info("creating index for messages")
            self.messages.create_index([('time', ASCENDING), ('user', ASCENDING)], unique=True)


    def __init__(self, truncate=False, messages_truncate=False, host_=None, port_=None, db_name_=None):
        if not host_ or not port_ or not db_name_:
            host_ = host
            port_ = port
            db_name_ = db_name

        database.__init__(self, host_, port_, db_name_)
        self._main_schema_ignition()
        if truncate:
            try:
                self.conn.drop_database(db_name_)

                self._main_schema_ignition()
            except Exception as e:
                log.exception(e)
                log.error('may be db_ignition must be?')
                raise e
        if messages_truncate:
            try:
                self.db.drop_collection(messages_info_name)
                self.db.drop_collection(messages_name)
                self._main_schema_ignition()
            except Exception as e:
                log.error('may be db_ignition must be?')
                log.exception(e)
                raise e


    def save_user(self, ser_user):
        """
        is serialised user from our model user
        """
        log.debug('saving user: un: %s; rn %s; tlc %s;' % (
            ser_user['name_'], ser_user['real_name'], ser_user['timeline_count']))
        son = SON(ser_user)
        saved_user = self.users.find_one({'name_': ser_user['name_']})

        if saved_user:
            son['_id'] = saved_user['_id']

        self.users.save(son)

    def get_user_by_name(self, user_name):
        user = self.users.find_one({'name_': user_name})
        if user:
            return m_user.create(user)
        return None

    def get_user(self, req):
        user = self.users.find_one(req)
        if user:
            return m_user.create(user)


    def save_diffs(self, ser_diffs):
        """
        saving diffs between one user in difference time
        in two collections - diffs (user_name, date_touch)
        and update users (add to set of diffs_)

        """
        log.debug('saving diffs' % ser_diffs)
        #user for updating
        #see algorithm of it generation #difference_machine
        #and methods
        #   form_id(), get_diff_id()
        #and in #m_user
        #   get_diff_part_id()
        diff_id = ser_diffs['diff_id_']
        left_name = diff_id['left']['name_']
        right_name = diff_id['right']['name_']
        if right_name != left_name:
            log.warn('i do not know what name is right %s --> %s ' % (left_name, right_name))
            return

        user = self.users.find_one({'name_': left_name})
        if user:
            self.users.update({'_id': user['_id']},
                    {"$addToSet": {'diffs_': {'id': ser_diffs['diff_id_'], 'datetime': datetime.datetime.now()}}})
            self.users.update({'_id': user['_id']}, {"$set": {'date_touch_': datetime.datetime.now()}})

            son = SON(ser_diffs)
            log.debug(son)
            self.diffs_output.save(son)
        else:
            log.warn('user for this diff not found...')

    def get_users_for_diff(self, use_input_diff_collection=props.prepared_collection, limit=10):
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
                user = m_user.create(self.users.find_one({'name_': diff['name_']}))
                users.append(user)
            return users
        else:
            user_objects = []
            if props.timedelta:
                more_than_it = datetime.datetime.now() - props.timedelta
                user_objects.extend(self.users.find({'date_touch_': {'$gte': more_than_it}}, limit=limit))

            if props.time_start and props.time_stop:
                user_objects.extend(self.users.find({'$and': [
                        {'date_touch_': {'$gte': props.time_start}},
                        {'date_touch_': {'$lte': props.time_stop}}
                ]}, limit=limit))

            users.extend([m_user.create(user) for user in user_objects])
            return list(set(users))

    def verify_user(self, name):
        user = self.users.find_one({'name_': name})
        if user:
            if user['date_touch_'] + props.min_timedelta > datetime.datetime.now():
                return m_user_status(m_user_status.s_updated, last_diff=user['date_touch_'])
            return m_user_status(m_user_status.s_update_needed, last_diff=user['date_touch_'])
        else:
            return m_user_status(m_user_status.s_none)

    def save_message(self, message):
        self.messages.save(message)

    def save_message_info(self, messages_info):
        self.messages_info.save(messages_info)

    def get_messages_by_user(self, user):
        #http://twitter.com/mrletemkno
        return [message for message in self.messages.find({'user': 'http://twitter.com/' + tools.imply_dog(str(user))})]

    def set_class(self, user, class_name):
        save_user = self.users.find_one({'name_': user})
        if save_user:
            self.users.update({'_id': save_user['_id']}, {'$set': {'class_name': class_name}})

    def get_not_loaded_users(self, batch=1000):
        users = []
        for user in self.users_not_loaded.find(limit=batch):
            users.append(user['name'])

        return users

    def set_user_loaded(self,user_name):
        self.users_not_loaded.remove({'name':user_name})