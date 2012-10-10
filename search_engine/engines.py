#-*- coding: utf-8 -*-
import webbrowser
import time
import  tweepy
from tweepy.error import TweepError
import vkontakte
from differences.diff_machine import difference_factory
import loggers
from model.db import db_handler
from model.tw_model import *
from properties import props
from properties.props import CONSUMER_SECRET, CONSUMER_KEY
import tools

__author__ = 'Alesha'

log = loggers.logger

class engine(object):
    def scrap(self, start_user, neighbourhood=props.def_n, level=0, relation_types=props.relation_types):
        pass











