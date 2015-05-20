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
    
    def __init__(self, sckt, address,name,dvector):
        # init things
        retry = 3
        data = ''
        self.name=name
        self.dvector = dvector
				super().__init__(sckt, address)
    
    def start(self):
        
        print('Connected by:', self.address)
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
       