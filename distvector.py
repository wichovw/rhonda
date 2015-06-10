import socket, threading
from wendy import Worker
from logger import logger
import time

config_file = [['A', '192.168.1.1', 5],
               ['B', '192.168.1.2', 8]]
INF = 99
US = 'C'

class Node:
    
    def __init__(self, name, address, cost):
        self.name = name
        self.address = address
        self.cost = cost
        self.updates = []

class DistVector:
    
    def __init__(self, config):
        self.nodes = {}
        for row in config:
            nod = Node(row[0], row[1], row[2])
            self.nodes[nod.name] = nod
        
        self.matrix = {}
        self.destinations = []
        for node in self.nodes:
            for nnode in self.nodes:
                key = (node, nnode)
                val = INF
                if node == nnode:
                    val = self.nodes[node].cost
                self.matrix[key] = val
            self.destinations.append(node)
                
            
    def dest(self, to, through):
        return self.matrix[(to, through)]
    
    def get_best(self, to):
        best = min(x for k, x in self.matrix.items() if k[0] == to)
        for name, node in self.nodes.items():
            if self.dest(to, name) == best:
                return (name, best)
            
    def update(self, name, changes):
        through = name
        updates = []
        for change in changes:
            to = change[0]
            cost = change[1]
            if to == US:
                continue
            if to not in self.destinations:
                for node in self.nodes:
                    self.matrix[(to, node)] = INF
                self.destinations.append(to)
            newval = self.nodes[through].cost + cost
            old_best = self.get_best(to)
            self.matrix[(to, through)] = newval
            new_best = self.get_best(to)
            if old_best != new_best:
                updates.append((to, new_best[1]))
        
        for name, node in self.nodes.items():
            node.updates.append(updates)
            
    def get(self, name):
        if len(self.nodes[name].updates):
            return self.nodes[name].updates.pop(0)
        return None

class DVWorker(Worker):
    
    def __init__(self, sckt, address, dvector):
        # init things
        retry = 3
        data = ''
        self.name=name
        self.dvector = dvector
        super().__init__(sckt, address)
    
    def start(self):
        logger.info('Connected by: %s' % self.address[0])
        thrd = threading.Thread(name='DVWorker-'+str(address), target=self.recv)
        thrd.start()
        while True:
            costs = self.dvector.get()
            if(costs==None):
                self.send("Type:KeepAlive~~")
            else:
                msg = ""
                for nodes in costs:
                    msg+=":".join(nodes)
                    msg+="~"
                msg+="~"
                self.send(msg)
            
            if(self.data!=''):
              self.retry=3
              splitted = self.data.split("~")
              type = splitted[1].split(":")[1]
              if(type=="DV"):
                nodes = []
                for i in range(2,len(splitted)):
                  node = splitted[i].split(":")
                  nodes.push([node[0],int(node[1])])
                self.dvector.update(self.name,nodes)
              elif(type=="KeepAlive"):
                retry=3
              
            else:
              retry-=1
            if(retry==0):
              thrd.join()
              exit()
            time.sleep(30) 
            
            
    def recv(self):
        chunks = []
        bytes_rcvd = 0
        while True:
            chunk = self.socket.recv(1024).decode('ascii')
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_rcvd += len(chunk)
            msg = self.iseof(chunks)
            if len(msg):
                self.data = msg
                msg = ''
            
if __name__ == "__main__":
    print('Test')
    dvector = DistVector(config_file)
    print('Forwarding table')
    print(dvector.matrix)
    dvector.update('B', [['C', 8],['D', 4]])
    print('Updated B')
    print(dvector.matrix)
    dvector.update('A', [['C', 5],['D', 3],['E', 4]])
    print('Updated A')
    print(dvector.matrix)
    for _ in range(5):
        print('Changes B')
        print(dvector.get('B'))
    
       