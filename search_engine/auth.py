import urllib
import lxml.html
import requests
from properties import props

__author__ = '4ikist'
class auth():
    """
    returning access tokens for vkontakte and facebook
    """
    def __init__(self):
        pass



    def get_vk_auth_token(self):
        params = {'client_id': props.vk_app_id,
                  'scope': 'friends,status,groups,messages,offline',
                  'redirect_uri': 'http://oauth.vk.com/blank.html',
                  'display': 'wap',
                  'response_type': 'token'}
        #getting oauth welcome
        r = requests.get('http://oauth.vk.com/authorize', params=params)
        post_params = self.__get_vk_first_parameters(r.text)
        post_params['email'] = props.vk_email
        post_params['pass'] = props.vk_password

        #get submit page
        r = requests.post('https://login.vk.com/?act=login&soft=1&utf8=1', post_params, cookies=r.cookies)
        if not self.__is_vk_login_success(r.text):
            url = self.__get_vk_action(r.text)
            url = urllib.unquote_plus(url)
            r = requests.post(url, cookies=r.cookies)
        #retrieve history of redirects
        return self.__retrieve_token(r.url)

    def get_fb_auth_token(self):
        params = {'client_id': props.fb_app_id,
                  'redirect_uri': 'https://www.facebook.com/connect/login_success.html',
                  'response_type': 'token'}
        r = requests.get('https://www.facebook.com/dialog/oauth', params=params)
        url, params = self.__get_fb_first_params(r.text)
        r = requests.post(url,params,cookies=r.cookies)
        return self.__retrieve_token(r.url)

    def __get_fb_first_params(self, text):
        doc = lxml.html.document_fromstring(text)
        form = doc.xpath('//form[@id="login_form"]')[0]
        inputs = form.xpath('//input')
        params = {}
        for input in inputs:
            params = dict(params, **{input.name: input.value})

        params['email'] = props.fb_email
        params['pass'] = props.fb_pass
        url = form.action
        return url, params

    def __get_vk_first_parameters(self, text):
        doc = lxml.html.document_fromstring(text)
        v_origin = doc.xpath('//input[@name="_origin"]')[0].value
        v_ip_h = doc.xpath('//input[@name="ip_h"]')[0].value
        v_to = doc.xpath('//input[@name="to"]')[0].value
        return {'_origin': v_origin, 'ip_h': v_ip_h, 'to': v_to}

    def __get_vk_action(self, text):
        doc = lxml.html.document_fromstring(text)
        action = doc.xpath('//form[@method="POST"]')[0].action
        return action

    def __is_vk_login_success(self, text):
        doc = lxml.html.document_fromstring(text)
        return doc.xpath('//body')[0].text.strip() == 'Login success'

    def __retrieve_token(self, url):
        return url[url.index('access_token=') + 13:url.index('&')]

