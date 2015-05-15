from wendy import Worker
from logger import logger

config_file = [['A', '192.168.1.1', 5],
               ['B', '192.168.1.2', 8]]

#class Node:
#    
#    def __init__(self, name, address, cost):
#        self.name = name
#        self.address = address
#        self.cost = cost
#
#class DistVector:
#    
#    def __init__(self, config):
#        self.nodes = []
#        for row in config:
#            row

class DVWorker(Worker):
    
    def __init__(self, sckt, address):
        # init things
        super().__init__(sckt, address)
    
    def start(self):
        logger.info('Connected by: %s' % self.address[0])
        while True:
            data = self.recv()
            logger.debug('Received cuz yolo %d bytes' % len(data))
            self.send(data)