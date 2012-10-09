from differences import diff_machine
from model.db import db_handler

__author__ = 'Alesha'
#todo create test for difference

difference_factory = diff_machine.difference_factory()

db = db_handler()
linoleum = db.get_user_by_name('@linoleum2k12')
print linoleum
chikist = db.get_user_by_name('@4ikist_')
print chikist

