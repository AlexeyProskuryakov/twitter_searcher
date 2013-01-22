# coding: utf-8

import requests
import loggers
from properties import props
from engines import engine
import json
from search_engine.auth import auth


__author__ = '4ikist'

log = loggers.logger
root_req_url = 'https://api.vk.com/method/'
fields = {'fields': 'first_name,last_name,nickname,sex,bdate,contacts,education,rate,counters'}

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

    def get_user_followings(self, uid):
        return self._call_method(uid, 'subscriptions.get', {'count': 1000})

    def get_user_followers(self, uid):
        return self._call_method(uid, 'subscriptions.getFollowers', {'count': 1000})

    def get_likes(self, uid):
        users = self._call_method(uid, 'fave.getUsers', fields)
        log.info(users)
        photos = self._call_method(uid, 'fave.getPhotos', {})
        log.info(photos)
        videos = self._call_method(uid, 'fave.getVideos', {})
        log.info(videos)
        posts = self._call_method(uid, 'fave.getPosts', {})
        log.info(posts)
        links = self._call_method(uid, 'fave.getLinks', {})
        log.info(links)


if __name__ == '__main__':
    o = auth()
    token = o.get_vk_auth_token()
    vk = vk_engine(token)
    vk.get_friends(props.vk_uid)

    vk.get_likes(props.vk_uid)

