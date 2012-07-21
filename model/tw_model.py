import time

__author__ = '4ikist'



class user(object):

    def __init__(self, name):
        self.date_ping = time.time()
        self.name = name
        self.followers_count = 0
        self.friends_count = 0
        self.list_count = 0
        self.tweets_count = 0
        self.tweets_stat = [] #statistic of user perls
        self.timeline = []
        self.followers_names = []
        self.friends_names = []
        self.lists_names = []

    def serialise(self):
        return self.__dict__

    def __str__(self):
        return 'name: %s, followers: %s, friends: %s, lists: %s, tweets_count: %s, \ntweet_stats: %s\nfollowers: %s\nfriends: %s, \nlists: %s' %\
               (self.name, self.followers_count, self.friends_count, self.list_count, self.tweets_count,
                self.tweets_stat, self.followers_names, self.friends_names, self.lists_names)





