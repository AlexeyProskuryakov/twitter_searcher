# coding: utf-8
import vkontakte
from properties import props
from engines import engine
__author__ = '4ikist'

class vk_engine(engine):
    def __init__(self):
        self.vk = vkontakte.API(props.vk_app_id,props.vk_app_secret)

    def scrap(self, start_user, neighbourhood=props.def_n, level=0, relation_types=props.relation_types):
        return self.vk.get('users.search',q = start_user)




if __name__ == '__main__':
    print vk_engine().scrap(u'Test')