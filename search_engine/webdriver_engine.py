from model.tw_model import m_user
from properties import props
from search_engine.engines import engine
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
import tools


class web_driver_engine(engine):
    def __init__(self, f_profile=props.ff_profile, implicitly_wait_time=5):
        self.driver = webdriver.Firefox(f_profile)
        self.driver.implicitly_wait(implicitly_wait_time)
        self.root_url = 'https://twitter.com/'
        self.init_engine()

    def init_engine(self):
        self.driver.get(self.root_url)


    def get_user_info(self, user):
        user_name = tools.imply_dog(user, False)
        self.driver.get(self.root_url + user_name)
        user = m_user(tools.imply_dog(user_name,True))

        followers = self.driver.find_element_by_xpath('//a[@data-element-term="follower_stats"]')
        followers_url = followers.get_attribute('href')

        user.followers_count = int(followers.find_element_by_xpath('/strong').text)
        print followers_url
        print user.followers_count


#        friends = self.driver.find_element_by_xpath('//a[@data-element-term="following_stats"]/strong')
#        user.friends_count = int(friends.text)
#
#        tweets = self.driver.find_element_by_xpath('//a[@data-element-term="tweet_stats"]/strong')
#        user.timeline_count = int(tweets.text)

        return user

    def scrap(self, start_user, neighbourhood=props.def_n, level=0):
        pass


class wd_exception(Exception):
    def __init__(self):
        Exception.__init__(self)


if __name__ == '__main__':
    engine = web_driver_engine()
    user = engine.get_user_info('linoleum2k12')
    print user.serialise()
