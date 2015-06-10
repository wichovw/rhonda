import socket, threading
from wendy import Worker
from logger import logger
import time

config_file = [['A', '192.168.1.1', 5],
               ['B', '192.168.1.2', 8]]
INF = 99
US = 'C'


class ForwardClass(Worker,dvector):
    
    def __init__(self, sckt, address):
        # init things
        self.dvector = dvector
        self.close = False
        self.data = ''
        super().__init__(sckt, address)
    
    def start(self):
        
        thrd = threading.Thread(name='ForwardWorker-'+str(address), target=self.recv)
        thrd.start()
        while !self.close:
          if(self.data!=''):
            msg = self.data
            splitted = self.data.split("~")
            #Get TO:
            toAddr = splitted[1].split(":")[1]
            
            ipaddress = self.dvector.forwarding(toAddr)
            if(ipaddress!=None):
              logger.info('Forwarding message to: %s' % ipaddress)
              s = socket.socket()
              s.connect((ipaddress,1981))
              s.send(msg)
              self.data = ''
              s.close()
            else:
              logger.info('Receiving message from: %s' % splitted[0].split(":")[1])
              s = socket.socket()
              s.connect(("127.0.0.1",1992))
              s.send(msg)
              self.data = ''
              s.close()
            self.close = True
            
            
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
      
      def close(self):
        return self.close

        
        

