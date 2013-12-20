import multiprocessing as mp
import zmq
import time
import numpy as np

from de import DifferentialEvolutionSP
from worker import DEWorker


class DEManager(object):

    def __init__(self, ports, work_count):
        self.send_port = ports['send']
        self.receive_port = ports['receive']
        self.control_port = ports['control']
        self.work_count = work_count

    def find_min(self, func_module, func_name, de_param):

        self._func_module = func_module
        self._func_name = func_name
        self._de_param = de_param

        vent_proc = mp.Process(target=self._vent, args=())
        sink_proc = mp.Process(target=self._sink, args=())
    
        vent_proc.start()
        sink_proc.start()
        vent_proc.join()
        sink_proc.join()

    def _vent(self):
        context = zmq.Context()
        vent_send = context.socket(zmq.PUSH)
        vent_send.bind('tcp://*:' + self.send_port)
        time.sleep(1)

        work_msg = dict(func_module = self._func_module,
                        func_name = self._func_name,
                        de_param = self._de_param)
 
        for i in range(self.work_count):
            vent_send.send_json(work_msg)

    def _sink(self):
        context = zmq.Context()

        result_receive = context.socket(zmq.PULL)
        result_receive.bind('tcp://*:' + self.receive_port)

        control_send = context.socket(zmq.PUB)
        control_send.bind('tcp://*:' + self.control_port)

        min_lst = []
        point_lst = []
        for i in range(work_count):
            result_msg = result_receive.recv_json()
            min_lst.append(result_msg['minimum'])
            point_lst.append(result_msg['min_point']) 
        control_send.send("STOP")

        cost = np.array(min_lst)
        x = np.array(point_lst)
        min_index = cost.argmin()
        print "min f", tuple(x[min_index]), "=", cost[min_index]



if __name__ == "__main__":
    work_count = 4 

    work_ports = dict(send='5558', receive='5557', control='5559')
    work = DEWorker('127.0.0.1', work_ports)
    for i in range(work_count):
        p = mp.Process(target=work.start, args=(i,)).start()

    mgr_ports = dict(send='5557', receive='5558', control='5559')
    mgr = DEManager(mgr_ports, 4)
    de_param = dict(pop_size=40, max_gen=1000, cr=0.9, f=0.9, proc_count=2)
    mgr.find_min('test_function','saddle',de_param)
