import json
import requests
import loggers
from search_engine.auth import auth
from search_engine.engines import engine

    #getting info by id
#can find by nick_name and id
#https://graph.facebook.com/100002078473949?fields=id,name,first_name,middle_name,last_name,gender,link,username,locale&access_token=AAACl954iVXsBAMmvAuHjI4xRySbYTBexFrGM5CmYdhdXuOyLp1hCZBGSwi517gQEI8GicVA7ZCy8y4m3bQckDpvpc5WB5WMAQbfQXVegZDZD
#
#user - *id,name,first_name,middle_name,last_name,gender,link,*username,locale
#page - feed (all wall), statuses, links, groups -- [name], notes -- [subject,message], posts(page posts), events -- [name,description]/
#event - description, name,owner,updated, [invited,feed]
# group - feed
#
#
#
###
__author__ = '4ikist'
root_url = 'https://graph.facebook.com/'
root_url_search = 'https://graph.facebook.com/search'
search_types = ['user', 'page', 'event', 'group','post']

log = loggers.logger

class fb_exception(Exception):
    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code

class fb_engine(engine):
    def __init__(self, access_token):
        log.info("access_token is '%s'" % access_token)
        self.access_token = access_token

    def __process_result(self, r):
        result = json.loads(r.text, encoding='utf-8')
        if result.has_key(u'error'):
            error = result[u'error']
            code = None
            if error.has_key(u'code'):
                code = error[u'code']
            raise fb_exception(error[u'message'], code)
        elif result.has_key(u'data'):
            return result[u'data']

    def __call_method(self, user_id, method):
        url = root_url + user_id + '/' + method
        params = {'access_token': self.access_token}
        r = requests.get(url, params=params)
        log.info("\ngetting: %s \nfor: %s\nurl: %s" % (method, user_id, r.url))
        return self.__process_result(r)

    def __call_search(self, query, type):
        url = root_url_search
        params = {'q': query, 'type': type, 'access_token': self.access_token}
        r = requests.get(url,params = params)
        log.info("searching...\nq: '%s'\ntype: %s\nurl: %s" % (query,type, r.url))
        return self.__process_result(r)

    #search_types = ['user', 'page', 'event', 'group']
    def search(self, query):
        try:
            for el in search_types:
                obj = self.__call_search(query,el)
                print obj
        except fb_exception as e:
            pass

if __name__ == '__main__':
    a = auth()
    token = a.get_fb_auth_token()
    fb = fb_engine(token)
    fb.search('spam')