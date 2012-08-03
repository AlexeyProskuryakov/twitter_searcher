import datetime
import re
import loggers
from properties import props

log = loggers.logger

__author__ = 'Alesha'

def _get_element(string):
    key = string[0]
    value = string[1:].strip()
    return key, value


def _is_message_element(str):
    if str[0] == 'T' or str[0] == 'U' or str[0] == 'W':
        return True
    return False


def extract_messages(file):
    log.info("reading file: %s" % file)
    f = open(file)
    lines = f.xreadlines()
    result = []
    buff = []
    for line in lines:
        if _is_message_element(line):
            buff.append(line)
            if len(buff) == 3:
                time = datetime.datetime.strptime(_get_element(buff[0])[1], props.ttr_time_format)
                user_url = _get_element(buff[1])[1]
                text = _get_element(buff[2])[1]
                result.append({'t': time, 'u': user_url, 'm': text})
                buff = []
    return result
smile_regexp = re.compile("\ {0,2}\:[\-\*]{0,1}[\)\(\*]+")

def get_count_smiles(input,regexp = smile_regexp):
    count = 0
    for el in input:
        count+=len(regexp.findall(el['m']))
    return count

if __name__ == '__main__':
    result = extract_messages("d:/temp/tweets2009-12.txt")
    print len(result)
    print get_count_smiles(result,smile_regexp)