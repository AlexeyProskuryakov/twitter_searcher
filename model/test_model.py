from datetime import datetime
from model.exceptions import model_exception
from model.tw_model import *
from tools import print_model_serializable
from model.diff_machine import create_difference

__author__ = '4ikist'



def test_users():
    user1 = m_user('@test1')

    user1.protected = True
    user1.real_name = 'Alesha'
    user1.inited_ = datetime.now()

    user1.list_count = 1
    user1.lists_names = ['list_1']

    user1.friends_count = 10
    user1.followers_count = 100

    user1.timeline_count = 10
    user1.timeline = [m_hash_dict({'text': 'text of timeline element 1', 'retweets': 10, 'initted': datetime.now()})]
    user1.timeline.append(m_hash_dict({'text': 'text of timeline element 2', 'retweets': 10, 'initted': datetime.now()}))

    user1.set_relations({'followers': ['fol_1', 'fol_2', 'fol_3'], 'friends': ['fr_1', 'fr_2', 'fr_3'],
                          'mentions': ['m_1', 'm_2', 'm_3']})

    user2 = m_user('@test1')

    user2.protected = True
    user2.real_name = 'Alesha'
    user2.inited_ = datetime.now()

    user2.list_count = 2
    user2.lists_names = ['list_1','list_2']

    user2.friends_count = 9
    user2.followers_count = 123

    user2.timeline_count = 11
    user2.timeline = [m_hash_dict({'text': 'text of timeline element 1', 'retweets': 10, 'initted': datetime.now()})]
    user2.timeline.append(m_hash_dict({'text': 'text of timeline element 2', 'retweets': 10, 'initted': datetime.now()}))
    user2.timeline.append(m_hash_dict({'text': 'text of timeline element 3', 'retweets': 11, 'initted': datetime.now()}))

    user2.set_relations({'followers': ['fol_1', 'fol_2', 'fol_4'], 'friends': ['fr_1', 'fr_2'],
                          'mentions': ['m_1', 'm_2', 'm_3', 'm_4']})

    return user1,user2

def test_diffs():
    user1, user2 = test_users()
    user3 = user1
    diff1_2 = create_difference(user1,user2)
    diff1_3 = create_difference(user1,user3)
    print_model_serializable(diff1_2)
    assert isinstance(diff1_2,m_difference)
    assert isinstance(diff1_3,serializable)

    assert not diff1_3.is_field('real_name')

    assert diff1_2.get_field('timeline')[difference_element.d_state] == difference_element.s_add

    user3.name_ = 'test1_'
    try:
        diff_bad = create_difference(user1,user3)
    except model_exception as e:
        assert e



def test_functions():
    pass


if __name__ == '__main__':
    test_diffs()