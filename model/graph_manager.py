from model.db import db_handler

class users_export():
    def __init__(self):
        self.handler = db_handler(host_='localhost',port_=27107)

    def form_nodes(self, f_name, parameter_f=lambda x: x['timeline_count']):
        file = open(f_name, 'w+')
        file.write("Label;Id;Weight;\n")
        f_users = self.handler.users.find()
        for user in f_users:
            file.write(user['name_'] + ";" + user['name_'] + ";" + str(parameter_f(user)) + "\n")
        file.close()
        print 'nodes formed'


    def form_edges(self, f_name):
        file = open(f_name, 'w+')
        file.write("Source;Target;Id;Directed\n")
        for user in self.handler.users.find():
            for out_ in user['friends_relations']:
                term = user['name_'] + ";" + out_ + ";;True\n"
                file.write(term)
            for in_ in user['followers_relations']:
                term = in_+';'+user['name_'] + ";;True\n"
                file.write(term)
        print 'edges formed'
        file.close()

if __name__ == '__main__':
    gr = users_export()
    gr.form_nodes('c:/temp/nodes.csv')
    gr.form_edges('c:/temp/edges.csv')