from wendy import Worker
import time

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
				retry = 3
				super().__init__(sckt, address)
    
    def start(self):
		
        print('Connected by:', self.address)

        while True:
						
						data = self.recv()
						if(!data):
								self.send("Keep alive")
						else:
							retry-=1
						if(retry==0):
							exit()
						time.sleep(30) 

       
						
