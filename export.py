from model.graph_manager import users_export
__author__ = '4ikist'

if __name__ == '__main__':
    gr = users_export()
    gr.form_nodes('c:/temp/nodes.csv')
    gr.form_edges('c:/temp/edges.csv')