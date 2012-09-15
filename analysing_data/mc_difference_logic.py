from differences.d_model import difference_element,m_hash_dict
from markov_chain_machine import markov_chain,element

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

* по сути уникальных слов

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


#todo realise
def compile_chain(markov_chain_):
    """
    executings for calculations frequency of markov chain/
    """
    for word in markov_chain_.words:
        word.f_weight = float(word.weight)/markov_chain_.words_count_
        word.f_rel_weight = float(sum([relation.weight for relation in markov_chain_._get_all_relations(word.mc_id)]))/float(sum([relation.weight for relation in markov_chain_._get_all_relations()]))

    for relation in markov_chain_.relations:
        relation.f_weight = float()


def diff_markov_chains(i_markov_chain,i_markov_chain_2):
    """
    for using into difference machine processing like
    difference_factory.add_i_function(diff_markov_chains)
    """
    diff_element = difference_element('mc_difference',None)

    nodes_left = set(i_markov_chain.words)
    nodes_right = set(i_markov_chain_2.words)

    intersection_nodes = nodes_left.intersection(nodes_right)
    symmetric_difference = nodes_left.symmetric_difference(nodes_right)

    edges_left = set(i_markov_chain.references)
    edges_right = set(i_markov_chain_2.references)

    intersection_edges = edges_left.intersection(edges_right)
    symmetric_difference = edges_left.symmetric_difference(edges_right)

    #tolerance

    #at first you must create markov chain at intersection nodes and edges
    markov_chain._create(intersection_nodes,intersection_edges)
    for intersection_node in intersection_nodes:
        relations_left_node = i_markov_chain.get_relations(intersection_node.content)
        relations_left_node.extend( i_markov_chain.get_relations(intersection_node.content,is_from = 1))

        relations_left_node = set(relations_left_node)


        relations_right_node = i_markov_chain_2.get_relations(intersection_node.content)
        relations_right_node.extend(  i_markov_chain_2.get_relations(intersection_node.content,is_from = 1))

        relations_right_node = set(relations_right_node)

        intersection_relations = relations_right_node.intersection(relations_right_node)
        symmetric_difference_relations = relations_right_node.symmetric_difference(relations_left_node)






