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
        self.physical_cost = cost
        self.updates = []
        self.client_conn = False
        self.server_conn = False
        
    def cost(self):
        if self.server_conn and self.client_conn:
            return self.physical_cost
        return INF

class DistVector:
    
    def __init__(self, config):
        self.nodes = {}
        self.name = US
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
                    val = 0
                self.matrix[key] = val
            self.destinations.append(node)
                
            
    def dest(self, to, through):
        return self.matrix[(to, through)] + self.nodes[through].cost()
    
    def get_best(self, to):
        best = min(x + self.nodes[k[1]].cost() for k, x in self.matrix.items() if k[0] == to)
        for name, node in self.nodes.items():
            if self.dest(to, name) == best:
                return (name, best)
            
    def update(self, name, changes):
        through = name
        updates = []
                
        for change in changes:
            to = change[0]
            cost = change[1]
            if to == self.name:
                continue
            if to not in self.destinations:
                for node in self.nodes:
                    self.matrix[(to, node)] = INF
                self.destinations.append(to)
            old_best = self.get_best(to)
            self.matrix[(to, through)] = cost
            new_best = self.get_best(to)
            if old_best != new_best:
                updates.append((to, new_best[1]))
            if to == through:
                for node in self.destinations:
                    updates.append((node, self.get_best(node)[1]))
        
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

    def connection_established(self, name, is_server):
        node = self.nodes[name]
        if is_server:
            node.server_conn = True
        else:
            node.client_conn = True
        if node.server_conn and node.client_conn:
            self.update(name, [(name, 0)])

            
    def connection_lost(self, name, is_server):
        node = self.nodes[name]
        if is_server:
            node.server_conn = False
        else:
            node.client_conn = False
        self.update(name, [(name, 0)])
            
    def get(self, name):
        total_changes = {}
        while len(self.nodes[name].updates):
            changes = self.nodes[name].updates.pop(0)
            for change in changes:
                to = change[0]
                cost = change[1]
                total_changes[to] = cost
        if not len(total_changes):
            return None
        return [(k, v) for k, v in total_changes.items()]
    
    def print_matrix(self):
        matrix = " "*5
        for node in sorted(self.nodes):
            matrix += "%4s "%node
        for node in sorted(self.destinations):
            matrix += "\n%4s "%node
            for ady in sorted(self.nodes):
                matrix += "%4s " % (self.matrix[(node, ady)] + self.nodes[ady].cost())
        return matrix

            
if __name__ == "__main__":
    print('Test')
    dvector = DistVector(config_file)
    print('Forwarding table')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.connection_established('B', True)
    print('B connected on my server side')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.connection_established('B', False)
    print('Connected to B as client')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.update('B', [['C', 8],['D', 4]])
    print('B Updated')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.connection_established('A', True)
    dvector.connection_established('A', False)
    print('A connected')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.update('A', [['C', 5],['D', 10],['E', 5]])
    print('A Updated')
    print(dvector.print_matrix())
    
    print('Send changes to B:')
    print(dvector.get('B'))
    
    dvector.connection_lost('B', False)
    print('B disconnected')
    print(dvector.print_matrix())
    
    print('Send changes to A:')
    print(dvector.get('A'))
    print('Send changes to B:')
    print(dvector.get('B'))
       