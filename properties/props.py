import os
import datetime

__author__ = '4ikist'

####    ttr api properties
CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

#at first start, delete it values and save new (it can see in logs by similar keys):
access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

#####   db properties
port = 27017
#host = '178.49.120.77'
host = 'localhost'
db_name = 'ttr'

#####   application properties
time_format = '%Y.%m.%d_%H:%M'
ttr_time_format = '%Y-%m-%d %H:%M:%S'

####    scrapper properties
def_n = 1   #default neighbourhood
relation_types = ['mentions', 'friends', 'followers']


####    web driver props
#implicitly_time = 5 #in sec
#ff_profile = webdriver.FirefoxProfile(os.path.dirname(__file__)+'/ff_profile') #profile for firefox with ttr account


####    diff props
#if it true - diff machine will be get users for diff from diff_users_input collection
prepared_collection = True
#if it False - get users for parameters:
timedelta = datetime.timedelta(days=10) #get users with date_touch_ between now-timedelta and now
time_start = datetime.datetime(2012, 8, 18) #
time_stop = datetime.datetime(2012, 8, 25) # and between time_start and time_stop

diff_batch_size = 10
min_timedelta = datetime.timedelta(days=1)

####    state properties
is_debug = True
is_client = True


def is_inited():
    if len(access_token)and len(access_token_secret):
        return True
    return False