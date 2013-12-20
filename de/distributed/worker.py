import zmq
from de import DifferentialEvolutionMP

class DEWorker(object):
    
    def __init__(self, manager_ip, ports):
        self.receive_addr = 'tcp://' + manager_ip + ':' + ports['receive']
        self.send_addr = 'tcp://' + manager_ip + ':' + ports['send']
        self.control_addr = 'tcp://' + manager_ip + ':' + ports['control']
         
    def start(self, i):
        context = zmq.Context()
 
        work_receive = context.socket(zmq.PULL)
        work_receive.connect(self.receive_addr)

        result_send = context.socket(zmq.PUSH)
        result_send.connect(self.send_addr)

        # Set up a channel to receive control messages over
        control_receive = context.socket(zmq.SUB)
        control_receive.connect(self.control_addr)
        control_receive.setsockopt(zmq.SUBSCRIBE, "")

        # Set up a poller to multiplex the work receiver and control receiver
        poller = zmq.Poller()
        poller.register(work_receive, zmq.POLLIN)
        poller.register(control_receive, zmq.POLLIN)
     
        # Loop and accept messages from both channels
        while True:
            socks = dict(poller.poll())

            if socks.get(work_receive) == zmq.POLLIN:
                print "Working:", i

                work_msg = work_receive.recv_json()
                module = __import__(work_msg['func_module'], 
                                    work_msg['func_name'])
                func = getattr(module, work_msg['func_name'])
                de_param = work_msg['de_param']

                algo = DifferentialEvolutionMP(de_param['pop_size'], 
                                               de_param['max_gen'],
                                               de_param['cr'], 
                                               de_param['f'],
                                               de_param['proc_count'])
     
                minimum, min_point = algo.find_min(func)
                result_msg = dict(minimum = minimum, 
                                  min_point = tuple(min_point))
                result_send.send_json(result_msg)

            if socks.get(control_receive) == zmq.POLLIN:
                control_message = control_receive.recv()
                if control_message == "STOP":
                    print "Worker", i, "stopped"
                    break

