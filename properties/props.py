__author__ = '4ikist'

####    ttr api properties
CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

#at first start, delete it values and save new (it can see in logs by similar keys):
access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

def is_inited():
    if len(access_token)and len(access_token_secret):
        return True
    return False

#####   db properties
port = 27017
host = '178.49.120.77'
#host = '127.0.0.1'
db_name = 'ttr'

#####   application properties
time_format = '%Y.%m.%d_%H:%M'

####    scrapper properties
def_n = 1   #default neighbourhood

is_debug = True