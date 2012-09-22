# coding=utf-8

from differences.d_model import difference_element, m_hash_dict
import loggers
from markov_chain_machine import markov_chain, element

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

def EL(node, node2, size):
    """
    now it use content. in owerriding it maybe more another
    """
    return float(node.weight + node2.weight) / size


def mc_size(mc1, mc2):
    if mc1.words_count_ == mc2.words_count_:
        return mc1.words_count_
    else:
        return float(mc1.words_count_ + mc2.words_count_) / abs(float(mc1.words_count_ - mc2.words_count_))


def sum_diff(elements, size_nodes, size_rel):
    sum = 0
    for el in elements:
        sum += float(el['node'].weight) / size_nodes + float(el['relation']) / size_rel
    return sum


def diff_markov_chains(_markov_chain_left, _markov_chain_right, EL=EL, size=mc_size):
    """
    for using into difference machine processing like
    difference_factory.add_i_function(diff_markov_chains)

    difference two mc:
    1) tolerance = by_intersection:( any_node in intersection EL of weights in input chains / their sizes + their siblings at 1..n
    which equals KnL = difference and intersection between their relations and nodes at another models / their sizes)
    + paths of intersection
    2) defence = by_differences:(any node in ... his weight / their sizes + their siblings at 1..n which equals Knl ... )
    """
    nodes_left = set(_markov_chain_left.get_nodes())
    nodes_right = set(_markov_chain_right.get_nodes())

    l_intersection_nodes = list(nodes_left.intersection(nodes_right))
    r_intersection_nodes = list(nodes_right.intersection(nodes_left))

    l_difference = nodes_left.difference(nodes_right)
    r_difference = nodes_right.difference(nodes_left)

    tolerance = 0
    defence = 0
    size = size(_markov_chain_left, _markov_chain_right)
    for i in range(len(l_intersection_nodes)):
        tolerance_el = EL(l_intersection_nodes[i], r_intersection_nodes[i], size)
        tolerance += tolerance_el


    def defence_F(_diff_elements, mc):
        """
        going for relations which incident of _diff_element[i]
        and getting weights for nodes which in difference and intersection
        """
        defence_ = 0
        tolerance_ = 0
        for l_diff_el in _diff_elements:
            false_defence = []
            true_defence = []

            defence_ += float(l_diff_el.weight) / float(mc.words_count_)
            #getting all relations which incident of this node
            relations = mc.get_relations_by_node_id(l_diff_el._id, from_=True, to_=True)
            rel_weight = 0
            for relation in relations:
                #getting adjacent of this node
                id = 0
                if relation.content[0] == l_diff_el._id:
                    id = relation.content[1]
                elif relation.content[1] == l_diff_el._id:
                    id = relation.content[0]
                rel_weight += relation.weight
                node_corr = mc.get_node_by_id(id)
                #imlying this node
                if node_corr in l_intersection_nodes:
                    false_defence.append({'node': node_corr, 'relation': relation})
                elif node_corr in l_difference:
                    true_defence.append({'node': node_corr, 'relation': relation})

            sum_false = sum_diff(false_defence, mc.words_count_, rel_weight)
            sum_true = sum_diff(true_defence, mc.words_count_, rel_weight)

            if sum_false > sum_true:
                defence_ += sum_true
            else:
                tolerance_ += sum_false

        return defence_, tolerance_

    ld, lt = defence_F(l_difference, _markov_chain_left)
    rd, rt = defence_F(r_difference, _markov_chain_right)

    tolerance += lt + rt
    defence += ld + rd
    diff_element = difference_element('mc_diff', {'tolerance': tolerance, 'defence': defence})
    return diff_element


