import datetime
import re
from time import sleep
from db_scripts.graph_model import text
import loggers
from model import functions
from model.db import db_handler
from properties import props
from model.functions import get_count_smiles
import tools

log = loggers.logger
#get from http://snap.stanford.edu/data/bigdata/twitter7/
__author__ = 'Alesha'

def _get_element(string):
    key = string[0]
    value = string[1:].strip()
    return key, value


def _is_message_element(str):
    if str[0] == 'T' or str[0] == 'U' or str[0] == 'W':
        return True
    return False


def extract_messages(file, to_what=db_handler(messages_truncate=True), limit=0):
    log.info("reading file: %s" % file)

    f = open(file)
    lines = f.xreadlines()
    result = []
    buff = []

    smile_buff = []
    count_all = 0
    count_messages = 0
    for line in lines:
        if _is_message_element(line):
            buff.append(line)
            if len(buff) == 3:
                time = datetime.datetime.strptime(_get_element(buff[0])[1], props.ttr_time_format)

                user_url = _get_element(buff[1])[1]
                user = user_url[user_url.rindex('/') + 1:]

                text_el = _get_element(buff[2])[1]
                if text_el != 'No Post Title':
                    words = functions.extracts_text_elements(text_el)
                    count_messages += 1
                else:
                    words = None

                count_all += 1

                if isinstance(to_what, db_handler):
                    db = to_what
                    db.save_message({'time': time,
                                     'user': tools.imply_dog(user, with_dog=True),
                                     'message': words})
                    smile_buff.append(functions.get_count_smiles(text_el))

                buff = []

        if  limit != 0 and count_all >= limit:
            break

    count_smiles = tools.sum_dicts(smile_buff)
    if isinstance(to_what, db_handler):
        to_what.save_message_info(
                {'smiles': tools.sum_dicts(smile_buff),
                 'count_all': count_all,
                 'count_messages': count_messages,
                 'date': datetime.datetime.now()})

    log.info("count all: %s, count smiles: %s" % (count_all, count_smiles))
    return result


if __name__ == '__main__':
    result = extract_messages("d:/temp/tweets2009-12.txt",limit=100000)
#    result = extract_messages("d:/temp/tweets2009-11.txt")
#    result = extract_messages("d:/temp/tweets2009-10.txt")

