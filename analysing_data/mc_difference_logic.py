# coding=utf-8

from differences.d_model import difference_element, m_hash_dict
import loggers
from markov_chain_machine import markov_chain, element
from model.db import db_handler, database
from properties.props import *

__author__ = 'Alesha'
__doc__ = """
markov chain difference logic implementing

и сказ о текстовых данных.


Два вида данных: 
@see https://github.com/AlexeyProskuryakov/twitter_searcher/blob/master/model/tw_model.py
1) Пользовательские данные: вида количеств различных связей, таких как:
    -кого читает
    -кто его читает
    -его упоминания
    -количества избранных людей, а также группы этих людей. 

    А также текстовых количеств:
    -количества сообщений
    -количества ссылок, тем и упоминаний в этом множестве.
    -скорости распространения информации. 
    # время, ревтиты, и прочая ересь. 


2) Текст: набор сообщений, и их некоторых параметров. 
По сути модель наследует раскрашенный мультиграф с весами как у узлов, так и у ребер. 
Данную модель реализует markov_chain and element classes in 
@see https://github.com/AlexeyProskuryakov/twitter_searcher/blob/master/analysing_data/markov_chain_machine.py

При этом, если рассматривать систему в общем, следует различать входные текстовые данные и выходные. 
То есть, что пользователь прочитал и что он написал.

Для реализации методов сравнения текстовых данных @see #видение социальной сети/#графово-иерархической модели 
потребуется находить разности между элементами этой модели. 

По сему было выдвинуты следующие обозначения: 

0) Так как в модели есть узлы и ребра, то присутствует как вес ребра так и вес узла. 
Вес узла, по сути является количеством употребления слова a_i. 
Вес ребра - количеством употребления слова a_i с другим словом a_i. 
Причем i и j принадлежит от 0 до n где n - количество уникальных слов (ребер) в савокупности сообщений. 
(#sp система поддерживает фразы, идущие подряд и все что душе угодно%) )
(#sp А если этот additional_object можно юзануть для хранений даты)


Обозначим ключевые параметры, на основе которых будет происходить вычисление разностей моделей. 
defence tolerante:
Из соображений множеств, считаем что пересечение этих множеств, с учетом синонимичных_преломлений*, будет являться 
их близостью, в кластеризационном плане. В то же время их разность будет являтся дальностью.

В будущем:
model_weight = model'_weight/model_nodes_count*
* или что-то типа

1) Коэффициент EL между двумя одинаковыми по значению узлами. Используется лишь для толерантности
EL(node,node') = (node.weight+node'.weight)*(model_weight / model'_weight)

2) Коэфиициент KL[i] между множествами узлов из разных моделей которые являются соседями рассматриваемых узлов. 
KL[i](node,node').

Требующий доступа до узлов и их связей. 
И состоящий из того же самого defence/tolerance 
Для толерантности - берем пересечение множеств их смежных узлов в разных моделях
Для защиты - разницу множеств их смежных узлов в разных моделях
При этом смежность зависит от i. 

I = all_nodes_near_at_i_depth(node,model).intersection(all_nodes_near_at_i(node,model'))

D = all_nodes_near_at_i_depth(node,model).difference(all_nodes_near_at_i_depth(node,model'))

Итак: 

KnL[i](node,node') = 

( sum_for_I(EL(node[j],node'[j])) * KrL[i] / 
( sum_for_D(node[k].weight/model_weight) + sum_for_D'(node[k'].weight/model'_weight) ) 



KrL[i] - является коэффициентом связей смежных узлов, подчиняющийся тем же законам - толерантности и защиты.
Следовательно: 
    KrL[i] = (summ_by_all_relations_between_I(rel.weight) - summ_for_D_relations(rel.weight)) / models_weights

Также нам потребуется знать глубины графа, т.е. максимальное количество i для коэффициентов: КrL[i] и KnL[i]

Итак формула для моделей: 

tolerance(model,model') = sum_by_intersection_of_their_nodes(EL(node,node')+(KnL[0],Knl[1],...))
defence(model,model') = sum_by_differences_of_their_nodes(node.weight/model_weight + (KnL[0],...)) 

По сути толерантность/защита при стремящимся нуле будет обозначать соответствие или не соответствие двух моделей. Однако
в виду того, что вышесказанные умозаключения не используют разности графовых параметров моделей, в дополнение, 
к коэффициентам толерантности/защиты следует использовать еще и количества сообщений затронутых в пересечением \ разницей 
множеств узлов модели. 

Поэтому:

tolerance(model,model') = sum_by_intersection_of_their_nodes(EL(node,node')+(KnL[0],Knl[1],...))
defence(model,model') = sum_by_differences_of_their_nodes(node.weight/model_weight + (KnL[0],...))



1) Модель поглощает другую модель и образуется класстер.
2) Модели расходятся

Таким образом P_clust(model_1,model_2) = f(tolerance,defence,counts_of_message)
Возможно что-то типа: 

    (tolerance/defence) / (model1_messages_all_sum)/(model2_messages_defence_summ) 

Встает вопрос про применение этой классификации: 
1) Класстеризация сообщений пользователя
2) Сравнение кластеризации пользователей с темами. 



"""
log = loggers.logger

class database_intersection_handler(database):
    #db booster for boosting intersection key - value
    state = ['not_loaded', 'loaded']

    def __init__(self, name):
        database.__init__(self, local_host, local_port, local_db_name)

        self.coll_left = self.db[str(name) + '_left']
        self.coll_right = self.db[str(name) + '_right']

        if self.coll_left.find_one() or self.coll_right.find_one():
            self.conn.drop_database(local_db_name)

        self.state_ = self.state[0]

    def load(self, intersection_left, intersection_right):
        for i in range(len(intersection_left)):
            left = intersection_left[i]._serialise()
            right = intersection_right[i]._serialise()
            self.coll_left.save(left)
            self.coll_right.save(right)
        self.state_ = self.state[1]

    def get_by_id(self, id, left=False):
        if left:
            d = self.coll_left.find_one({'_id': id})
            if d:
                return element.create(d)
            return None
        if right:
            d = self.coll_left.find_one({'_id': id})
            if d:
                return element.create(d)
            return None


    def un_load(self):
        self.conn.drop_database(db_name_)
        self.state_ = self.state[0]

#interested functions.....
def diff_size(mc1, mc2):
    if mc1.words_count_ == mc2.words_count_:
        return 1
    else:
        return abs(float(mc1.words_count_ - mc2.words_count_))


def EL(node1, node2, mc1, mc2, diff_size=diff_size):
    """
    now it use content. in owerriding it maybe more another
    """
    return float(node1.weight + node2.weight) / diff_size(mc1, mc2)


def N_def_tol(defence, tolerance, _markov_chain_left, booster_int, booster_diff, l_difference, left, EL=EL):
    for l_d_element in l_difference:
        #get incident edges
        relations = _markov_chain_left.get_relations_by_node_id(l_d_element._id)
        sum_rel = sum([rel.weight for rel in relations])
        defence += l_d_element.weight
        for relation in relations:
            rel_koeff = (float(relation.weight) / sum_rel)
            #if adjacent element in
            adjacent_el_id = relation.get_adjacent(l_d_element._id)
            adjacent_el_ = booster_int.get_by_id(adjacent_el_id, left=left)
            if adjacent_el_:
                tolerance += EL(l_d_element, adjacent_el_, _markov_chain_left, _markov_chain_right) * rel_koeff
            else:
                adjacent_el_ = booster_diff.get_by_id(adjacent_el_id, left=left)
                defence += EL(l_d_element, adjacent_el_, _markov_chain_left, _markov_chain_right) * rel_koeff
    return defence, tolerance


def main_function(defence, tolerance, mc_1, mc_2):
    uniq_left = sum(mc_1.get_unique_nodes_edges())
    uniq_right = sum(mc_2.get_unique_nodes_edges())

    k_unique = (float(uniq_left) / mc_2.words_count_ + float(uniq_right) / mc_2.words_count_)
    return float(abs(defence - tolerance)) * k_unique


def diff_markov_chains(_markov_chain_left, _markov_chain_right, EL=EL):
    """
    for using into difference machine processing like
    difference_factory.add_i_function(diff_markov_chains)

    difference two mc:
    1) tolerance = by_intersection:( any_node in intersection EL of weights in input chains / their sizes + their siblings at 1..n
    which equals KnL = difference and intersection between their relations and nodes at another models / their sizes)
    + paths of intersection
    2) defence = by_differences:(any node in ... his weight / their sizes + their siblings at 1..n which equals Knl ... )
    """
    booster_int = database_intersection_handler('intersection')
    booster_diff = database_intersection_handler('difference')

    nodes_left = set(_markov_chain_left.get_nodes())
    nodes_right = set(_markov_chain_right.get_nodes())

    #intersection and difference sets of elements (@see mc_model.element class)
    l_intersection_nodes = list(nodes_left.intersection(nodes_right))
    r_intersection_nodes = list(nodes_right.intersection(nodes_left))

    l_difference = nodes_left.difference(nodes_right)
    r_difference = nodes_right.difference(nodes_left)

    #and boost them
    booster_diff.load(list(l_difference), list(r_difference))
    booster_int.load(list(l_intersection_nodes), list(r_intersection_nodes))

    tolerance = 0
    defence = 0
    log.info()
    for i in range(len(l_intersection_nodes)):
        tolerance += EL(l_intersection_nodes[i], r_intersection_nodes[i], _markov_chain_left, _markov_chain_right)

    dl, tl = N_def_tol(defence, tolerance, _markov_chain_left, booster_int, booster_diff, l_difference, True)
    dr, tr = N_def_tol(defence, tolerance, _markov_chain_right, booster_int, booster_diff, r_difference, False)

    defence += dl
    defence += dr

    tolerance += tl
    tolerance += tr

    result = main_function(defence, tolerance, _markov_chain_left, _markov_chain_right)

    booster_diff.un_load()
    booster_int.un_load()

    return difference_element(None, result)