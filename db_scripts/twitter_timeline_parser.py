import loggers
from model.db import db_handler
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


def extract_messages(file, to_what=db_handler(messages_truncate=True), limit=10):
    f = open(file)
    users = set()
    message = None

    line = f.readline()
    while line:
        if _is_message_element(line):
            if not message:
                message = {}
            element = _get_element(line)
            if element[0] == 'T':
                message['time'] = element[1]
            elif element[0] == 'U':
                user = element[1]
                message['user'] = user[user.index('twitter.com') + len('twitter.com') + 1:]
            elif element[0] == 'W':
                message['words'] = element[1]
        if message and len(message) == 3:
            if message['words'] != 'No Post Title':
                if to_what:
                    log.debug('save message > %s'%message)
                    to_what.save_message(message)
                users.add(message['user'])
                message = None
        line = f.readline()
    return users


if __name__ == '__main__':
    result = extract_messages("c:/temp/tweets2009-12.txt")
    user = set(tools.flush(result, by_what=lambda x:x['user']))



