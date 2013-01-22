from pymongo import ASCENDING
import loggers
from model.db import database
import datetime
import re
from visualise.vis2d_machine import visualise
import math

__author__ = '4ikist'
log = loggers.logger
format = '%d-%m-%Y %H:%M'


def load_data(file_name, out):
    f = open(file_name, 'r')
    lines = f.xreadlines()

    user = None
    for line in lines:
        row = unicode(line, encoding='cp1251')

        if 'ID' in row:
            user = {'_id': row[row.index(':') + 1:].strip()}
        if 'Username' in row:
            user['name'] = row[row.index(':') + 1:].strip()
        if 'RealName' in row:
            user['real_name'] = row[row.index(':') + 1:].strip()

        if '======mail.ru====' in row:
            if user:
                out.save(user)
                user = None


def __convert(input):
    if 'x x' not in input:
        return datetime.datetime.strptime(input, format)
    else:
        return None

#IP 188.242.214.234 Mir 23-08-2010 08:08 regis 23-08-2010 16:08 parole x x blocked 23-08-2010 16:08 user 264246714 000000000000000000000.0@mail.ru
def fill_id_params(filename, out):
    f = open(filename, 'r')
    lines = f.xreadlines()
    for line in lines:
        row = unicode(line)

        ip_ind = row.index('IP')
        mir_ind = row.index('Mir')
        regis_ind = row.index('regis')
        parole_ind = row.index('parole')
        blocked_ind = row.index('blocked')
        user_ind = row.index('user')

        ip = [int(el) for el in row[ip_ind + 2:mir_ind].strip().split('.')]

        mir_created = row[mir_ind + 3:regis_ind].strip()
        registration = row[regis_ind + 5:parole_ind].strip()
        pass_changed = row[parole_ind + 6:blocked_ind].strip()
        blocked_time = row[blocked_ind + 7:user_ind].strip()
        user_prep = row[user_ind + 4:].strip()
        sem_ind = user_prep.index(' ')
        user_id = user_prep[:sem_ind].strip()
        user_name = user_prep[sem_ind:user_prep.index('@')].strip()

        result = {'_id': user_id,
                  'name': user_name, 'ip': ip,
                  'mir_init': __convert(mir_created),
                  'reg_init': __convert(registration),
                  'block_init': __convert(blocked_time),
                  'pass_changed': __convert(pass_changed)}

        out.save(result)


def fill_attribute(filename, out, attribute=None):
    if not attribute: attribute = {'banned': True}

    f = open(filename, 'r')
    lines = f.xreadlines()
    for line in lines:
        print line
        row = str(line)
        row = row[:row.find('@')]
        out.add_attribute({'name': row.strip()}, attribute)

def _is_normal(i):
    pass

class mirs_rb(database):
    def __init__(self, host_, port_, db_name_):
        database.__init__(self, host_, port_, db_name_)
        self.users = self.db['mir_users']
        if not self._is_index_presented(self.users):
            log.info("creating index for users")
            self.users.create_index('name', ASCENDING, unique=True)

        self.clust = self.db['clust']

    def save(self, user):
        log.info('saving user %s' % user)
        self.users.save(user)

    def add_attribute(self, req, attribute):
        log.info('updating user %s field %s' % (req, attribute))
        user = self.users.find_one(req)
        if user:
            self.users.update(req, {'$set': attribute})
        else:
            user = dict(req, **attribute)
            self.users.save(user)


            #{'name': u'venecia_91', 'ip': [90, 188, 199, 129], 'block_init': datetime.datetime(2010, 5, 24, 21, 59), 'reg_init': datetime.datetime(2008, 2, 8, 17, 50), 'mir_init': datetime.datetime(2008, 2, 8, 11, 50), '_id': u'83382519', 'pass_changed': datetime.datetime(2010, 6, 10, 9, 3)}

    def process(self):
        reg = re.compile('^[a-z]+\d+$')
        reg_w = re.compile('[a-z]+')
        reg_d = re.compile('\d+')
        users = self.users.find({'name': {'$regex': '^[a-z]+[0-9]+$'}})
        names_classes = {}
        count = 0
        normal = 0
        for user in users:
            name = user['name']
            if reg.match(name):
                count += 1
                chars = reg_w.findall(name)[0]
                digits = int(reg_d.findall(name)[0])
                if (digits > 1900 and digits < 2012) or (digits > 10 and digits < 100):
                    normal += 1

                if names_classes.has_key(chars):
                    x = names_classes[chars]
                    x.append(digits)
                else:
                    names_classes[chars] = [digits]

        max = 0
        for key in names_classes.iterkeys():
            arr = names_classes[key]
            print 'save', key
            if len(arr) > max:
                max = len(arr)
            try:
                self.clust.save({'_id': key, 'value': arr})
            except Exception:
                pass
        print 'count', count, 'normal', normal, 'max', max

    def visualise_clust(self, max):
        points = []
        for i in range(max):
            x = i
            y = self.clust.find({'value': {'$size': i}}).count()
            if (y < 100):
                continue
            points.append({'x': x, 'y': y})
            print x, y
        visualise(points, header='count of names and', x_title='count of variable digits',
            y_title='count of cluster names')

    def fill_entropy(self):
        count_all = self.clust.find().count()
        for el in self.clust.find({'entropy':{'$exists':False}}):
            val = el['value']
            #calulate entropy
            sum = 0
            for el_val in val:
                p = float(self.clust.find({'value': el_val}).count()) / count_all
                sum += (p * math.log(p, 2))
            entropy = sum * -1
            self.clust.update(el, {'$set': {'entropy': entropy}})
            log.info('cluster_name: %s; entropy: %s'%(el['_id'],entropy))

    def visualise_entropy(self):
        #todo visualise without normal values
        points = []
        for el in self.clust.find({'entropy':{'$exists':True}}):

            x = len(el['value'])
            y = el['entropy']
            points.append({'x':x,'y':y})
        visualise(points,x_title='count of variable digits',y_title='entropy')
    def visualise_digits_count(self):
        points = []
        for el in self.db['clust_values'].find():
            x = el['_id']
            y = el['value']['count']
            points.append({'x':x,'y':y})
        visualise(points,x_title='digit',y_title='count in usernames')



def get_digits(input):
    pass

#count 959539 normal 205391 max 1448
if __name__ == '__main__':
    from properties.props import *

    out = mirs_rb(host, port, db_name)
    #load_data('D:\\aspiranture\\data\\_spam_tools\\deleted_mirs_info',out)
    #fill_attribute('D:\\aspiranture\\data\\_spam_tools\\banned', out, {'banned': True})
    #fill_attribute('D:\\aspiranture\\data\\_spam_tools\\blocked', out, {'blocked': True})
    #fill_id_params('D:\\aspiranture\\data\\_spam_tools\\ids.log', out)
    #out.process()
    #out.visualise_clust(1448)
    #out.fill_entropy()
    out.visualise_digits_count()