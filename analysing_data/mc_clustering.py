from analysing_data import markov_chain_machine
from analysing_data.markov_chain_machine import markov_chain
from analysing_data.mc_difference_logic import diff_markov_chains
from analysing_data.redis_handlers import model_handler
from model.db import db_handler
import text_proc.text_processing as tp
import tools
import time

__author__ = '4ikist'

booster = model_handler(truncate=True)

def clust(models):
    out = []
    for mc in models:
        t1 = time.time()

        nearest = max([{el: diff_markov_chains(mc.model_id_, el.model_id_, booster)} for el in models if el != mc],
            key=lambda x: x.values()[0])
        nearest.keys()[0].print_me()
        print nearest.values()[0]
        new_mc_id = booster.sum_models(mc.model_id_, nearest.keys()[0].model_id_)
        new_mc = markov_chain(new_mc_id, booster)
        out.append(new_mc)

        t2 = time.time()
        print 'time: ', t2 - t1
    return clust(out)


def prep_models(timeline):
    return [markov_chain_machine.create_model([message], hash(str(message)), booster) for message in timeline]

#if __name__ == '__main__':
#    db = db_handler(host_='localhost', port_=27017, db_name_='ttr_exp')
#    user = db.get_user({'name_': '@GoogleRussia'})
#    timeline = tools.flush(user.timeline, by_what=lambda x: tp.get_words(x['text'], is_normalise=True))
#    print len(timeline)
#    models = prep_models(timeline)
#    models = clust(models)



import random
import multiprocessing
import time

class Worker(multiprocessing.Process):
    def __init__(self, work_queue, result_queue):
        # base class initialization
        multiprocessing.Process.__init__(self)

        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            # get a task
            #job = self.work_queue.get_nowait()
            try:
                job = self.work_queue.get_nowait()
            except Exception:
                break

            # the actual processing
            print("Starting " + str(job) + " ...")
            delay = random.randrange(1, 3)
            time.sleep(delay)

            # store the result
            self.result_queue.put(delay)

if __name__ == "__main__":
    num_jobs = 20
    num_processes = 8

    # run
    # load up work queue
    work_queue = multiprocessing.Queue()
    for job in range(num_jobs):
        work_queue.put(job)

    # create a queue to pass to workers to store the results
    result_queue = multiprocessing.Queue()

    # spawn workers
    for i in range(num_processes):
        worker = Worker(work_queue, result_queue)
        worker.start()

    # collect the results off the queue
    results = []
    for i in range(num_jobs):
        print(result_queue.get())