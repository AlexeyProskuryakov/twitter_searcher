__author__ = 'Alesha'
import graph_model

text = graph_model.text('a b c d e f g h a b c d')
print text.get_path('a','g')
print text.get_path('a','g',reverse=True)
print text.get_path_between('e',5,5,5)
print text.get_count_element_unique()
print text.get_count_element_all()
print text.get_count_element('d')