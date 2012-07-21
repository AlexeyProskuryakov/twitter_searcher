from model import diff_machine
from model.graph_manager import db_graph
from model.db import db_handler

from model.diff_machine import difference, difference_element
from model.tw_model import user

__author__ = 'Alesha'

user1 = None
user2 = None
user3 = None
diff1_2 = None
#test_model: followers_count_diff +1, friends_count_diff +3,
#   followers_names_diff [no grow]
#   friends_names_diff [rem: fr_two, add: fr_two_next]

#diff1_3 = difference(user1, user3)
#diff2_3 = difference(user2, user3)
#diff3_1 = difference(user3, user1)
class test():
   
    def test_model(self):
        user1 = user('test')
        user1.followers_count = 1
        user1.friends_count = 2
        user1.followers_names.append('fol_one')
        user1.followers_names.append('fol_two')
        user1.followers_names.append('fol_three')

        user1.friends_names.append('fr_one')
        user1.friends_names.append('fr_two')
        self.user1 = user1

        user2 = user('test')
        user2.followers_count = 2
        user2.friends_count = 5
        user2.followers_names.append('fol_one')
        user2.followers_names.append('fol_two')
        user2.followers_names.append('fol_three')
        user2.friends_names.append('fr_one')
        user2.friends_names.append('fr_two_next')
        self.user2 = user2

        user3 = user('test')
        user3.followers_count = 8
        user3.friends_count = 9
        user3.followers_names.append('fr_three')
        user3.followers_names.append('fr_two')
        user3.followers_names.append('fr_one')
        user3.followers_names.append('fr_one_new')
        user3.followers_names.append('fr_two_new')

        user3.friends_names.append('fol_one_new')
        user3.friends_names.append('fol_two')
        user3.friends_names.append('fol_two_new')
        self.user3 = user3

        print user1
        print user1.serialise()

        diff1_2 = difference(user1, user2)
        assert type(diff1_2.diff_int(2, 3)) == type(difference_element(None, None))

        #followers_count_diff +1, friends_count_diff +3,

        assert diff_machine.s_grow == diff1_2.get_state_by_field_name("friends_count")

        assert 3 == diff1_2.get_all_content_by_field_name("friends_count")

        #   followers_names_diff [no grow]
        assert diff_machine.s_no_grow in diff1_2.get_state_by_field_name("followers_names")

        #   friends_names_diff [rem: fr_two, add: fr_two_next]
        assert {diff_machine.d_state: diff_machine.s_a_new,
                diff_machine.d_content: ['fr_two_next']} in diff1_2.get_all_content_by_field_name('friends_names')

        self.diff1_2 = diff1_2

    def test_graph_creation(self):
        db_handler = db_graph()
        db_handler.form_edges("d:/temp/edges.csv")
        db_handler.form_nodes("d:/temp/nodes.csv")


    def test_db(self):
        db = db_handler()
        self.test_model()
        db.save_user(self.user1.serialise())
        db.save_user(self.user2.serialise())
        db.save_user(self.user3.serialise())
        db.save_diffs(self.diff1_2.serialise())

if __name__ == '__main__':
    test = test()
    test.test_model()
    test.test_db()