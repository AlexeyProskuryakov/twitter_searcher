from differences.d_model import difference_element,m_hash_dict
from markov_chain_machine import markov_chain,element

__author__ = 'Alesha'
__doc__ = """
markov chain difference logic implementing

Два вида данных: 
@see https://github.com/AlexeyProskuryakov/twitter_searcher/blob/master/model/tw_model.py
1) Пользовательские данные вида количеств различных связей, таких как:
    -кого читает
    -кто его читает
    -его упоминания
    -количества избранных людей, а также группы этих людей. 

    А также текстовых количеств:
    -количества сообщений
    -количества ссылок, тем и упоминаний в этом множестве.
    # время, ревтиты, и прочая ересь. 


2) Текст: набор сообщений, и их некоторых параметров. 
Преобразованный в вид который реализует markov_chain and element classes in 
@see https://github.com/AlexeyProskuryakov/twitter_searcher/blob/master/analysing_data/markov_chain_machine.py

По сути модель наследует раскрашенный мультиграф с весами как у узлов, так и у ребер. 

При этом, для реализации гипотезы 
@see #видение социальной сети/#графово-иерархической модели 
потребуется находить разности между элементами этой модели. 

По сему было выдвинуты следующие обозначения: 
#todo using nodes start and stop?
0) Так как в модели присутствуют узлы и ребра, то присутствует как вес ребра так и вес узла. 
Вес по своей сути является количеством употребления слова a_i. 
Вес ребра - количеством употребления слова a_i с другим словом a_i. 
Причем i и j принадлежит от 0 до n где n - количество уникальных слов (#sp система поддерживает фразы, идущие
подряд и все что душе угодно%) ) в савокупности сообщений. 


(#sp А если этот additional_object можно юзануть для хранений даты, не? Тогда все перестраивать найух)


1) Суммы весов и суммы частот пересечений и разниц множеств как всей модели так и окружающих определенного узла модели. 
2) 


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






