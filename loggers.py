__author__ = '4ikist'
import logging, logging.handlers, sys, os
import datetime

level_std = logging.DEBUG
level_fname = logging.INFO
filename = '/logs/'+datetime.datetime.now().strftime('%Y_%m_%d')+".log"

class log(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            fname = os.path.dirname(__file__)+filename

            __log_obj=logging.getLogger('main')
            __log_obj.setLevel(level_std)
            __formatter=logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\': %(message)s','%Y-%m-%d %H:%M:%S')

            __handler=logging.StreamHandler(sys.stdout)
            __handler.setFormatter(__formatter)
            __log_obj.addHandler(__handler)

            __handler=logging.FileHandler(fname, 'w+')
            __handler.setFormatter(__formatter)
            __handler.setLevel(level_fname)
            __log_obj.addHandler(__handler)

            cls._log_object = __log_obj
            cls._file_name = fname
            cls._instance = super(log, cls).__new__(cls)

        return cls._instance

   


logger = log()._log_object
logger.info("!!! start logging at %s !!!"%log()._file_name)

if __name__ == '__main__':
    pass


