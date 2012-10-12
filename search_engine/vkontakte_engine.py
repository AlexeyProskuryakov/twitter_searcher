# coding: utf-8
import urllib
import requests
from properties import props
from engines import engine
import lxml.html
import json
import md5
from search_engine.auth import auth

__author__ = '4ikist'

root_req_url = 'https://api.vk.com/method/'
fields = {'fields': 'first_name,last_name,nickname,sex,bdate,contacts,education,rate'}

class vk_exception(Exception):
    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code


class vk_engine(engine):
    def __init__(self, access_token):
        self.access_token = access_token

    def _call_method(self, user_id, name, method_params):
        url = root_req_url + name
        params = {'uid': user_id,
                  'access_token': self.access_token}
        params = dict(params, **method_params)
        response = requests.post(url, params)
        response_json = json.loads(response.text, encoding='utf-8')

        if response_json.has_key('response'):
            return response_json['response']
        else:
            message = response_json[u'error'][u'error_msg']
            code = response_json[u'error'][u'error_code']
            raise vk_exception(message, code)

    def get_friends(self, uid):
        return self._call_method(uid, 'friends.get', fields)

    def get_wall(self, uid):
        return self._call_method(uid, 'wall.get', {'owner_id': uid, 'extended': 1})

    def get_user_data(self, uid):
        return self._call_method(uid, 'getProfiles', fields)

if __name__ == '__main__':
    o = auth()
    token = o.get_vk_auth_token()
    vk = vk_engine(token)

    print vk.get_user_data(props.vk_uid)
    friends = vk.get_friends(props.vk_uid)
    for friend in friends:
       print  vk.get_wall(friend[u'uid'])
    print vk.get_wall(props.vk_uid)
