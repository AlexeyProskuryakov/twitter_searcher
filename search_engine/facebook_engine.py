import json
import requests
import loggers
from search_engine.auth import auth
from search_engine.engines import engine

#user - id,name,first_name,middle_name,last_name,gender,link,username,locale
#user_connections - friends, posts, subscribedto, subscribers

#page

#post - id, from, to, message, message_tags, likes, type,
#post_connections - likes, comments

#event - id, owner, name, description, location,
#event_connections - feed, noreply, invited, attending, maybe, declined

#group - id, owner, name, description, link
#group_connections - feed, members, docs
#
###
__author__ = '4ikist'
root_url = 'https://graph.facebook.com/'
root_url_search = 'https://graph.facebook.com/search'
search_types = ['user', 'page', 'event', 'group', 'post']

log = loggers.logger



class page():
    connections =  ['notes', 'posts', 'statuses', 'questions']
    fields = ['name', 'likes', 'phone', 'talking_about_count', 'website']
    def __init__(self):
        self.id = None
        self.name = None

        self.phone = None
        self.website = None

        self.likes = None
        self.talking_about_count = None

    def get_fields(self):
        fields = self.__dict__
        return fields

    def set_field(self, field_name, field_value):
        self.__dict__[field_name] = field_value

    def add_own_data(self, data):
        self.own_data_ = data

    def add_external_data(self, data):
        self.external_data_ = data

    def __str__(self):
        return 'page: '+self.name+" ["+self.id+"]\n"+str(self.__dict__)+'\n'

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

    def __call_method(self, id, connection):
        url = root_url + id + '/' + connection
        params = {'access_token': self.access_token}
        r = requests.get(url, params=params)
        log.info("\n connection: %s \n for: %s\n url: %s" % (connection, id, r.url))
        return self.__process_result(r)

    def __call_search(self, query, type, additional_params=None):
        if not additional_params: additional_params = {}

        url = root_url_search
        params = {'q': query, 'type': type, 'access_token': self.access_token}
        params = dict(params, **additional_params)
        r = requests.get(url, params=params)
        log.info("searching...\nq: '%s'\ntype: %s\nurl: %s" % (query, type, r.url))
        return self.__process_result(r)

    def imply_page(self, input_data):
        if not isinstance(input_data, dict):
            return None
        else:
            sprout_page = page()
            p_fields = sprout_page.get_fields()
            for el in p_fields.keys():
                if input_data.has_key(el):
                    sprout_page.set_field(el, input_data[el])
            return sprout_page

            #search_types = ['user', 'page', 'event', 'group']

    def search_pages(self, query):
        pages = self.__call_search(query, 'page',
            {'fields': 'name, likes, phone, talking_about_count, website, checkins'})
        for page_el in pages:
            s_page = self.imply_page(page_el)

            log.info(s_page)
            #getting connections
            for connection in page.connections:
                page_conn = self.__call_method(s_page.id,connection)
                log.info(page_conn)


if __name__ == '__main__':
    a = auth()
    token = a.get_fb_auth_token()
    fb = fb_engine(token)
    fb.search_pages('test')