import re
import os


__author__ = 'Alesha'
path_name = os.path.join(os.path.dirname(__file__)).replace('\\', '/')


def create_commands():
    f = open(path_name + '/search_engine/commands.py'.replace('\\', '/'))
    lines = f.readlines()
    out_lines = []
    for line in lines:
        if line[0] == '#':
            out_lines.append(line+'\n')
        elif len(line):
            strings = re.compile('[a-zA-Z0-9/]+').findall(line)
            print strings
            if len(strings) > 5:
                method = strings[0]
                name = strings[1]
                description = strings[2:]
                op_name = '_'.join(entity for entity in re.compile('[a-z]+').findall(name))
                comment = method + ',' + ' '.join(description)
                code = op_name + ' = ' + "'" + name + "'"
                out_lines.append("#"+comment+'\n')
                out_lines.append(code+'\n')
    for line in out_lines:
        print line

    f.close()
    g = open(path_name + '/serch_engine/commands_.py'.replace('\\', '/'),'w+')
    g.writelines(out_lines)
    g.close()
if __name__ == '__main__':
    create_commands()