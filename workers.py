from logger import logger
import time

class Worker:
    
    def __init__(self, sckt, address):
        self.socket = sckt
        self.address = address
        
    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.socket.send(msg[totalsent:].encode('ascii'))
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent += sent
        logger.debug('SEND: %s' % msg)
        
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
                break
        logger.debug('RECV: %s' % msg)
        return msg
    
    def iseof(self, chunks):
        msg = ''.join(chunks).strip()
        if '~~' in msg:
            return msg[:msg.find('~~')]
        return []
        
    def parse(self, msg):
        lines = msg.split('~')
        message = {}
        for line in lines:
            term, desc = line.split(':', maxsplit=1)
            message[term.lower()] = desc
        return message
    
    def render(self, message):
        from_ = message.get('from', None)
        type = message.get('type', None)
        if from_ and type:
            msg = '~'.join(['From:%s'%from_, 'Type:%s'%type])
            return '%s~~' % msg
    
    def start(self):
        # this method should be overriden
        logger.info('Connected by: %s' % self.address[0])
        while True:
            data = self.recv()
            logger.debug('Received %d bytes' % len(data))
            self.send(data)      
            
class ClientWorker(Worker):
    
    def __init__(self, sckt, address, dvector):
        self.dvector = dvector
        super().__init__(sckt, address)
        
    def start(self):
        logger.info('Connected as client to: %s' % self.address)
        self.send(self.render({'from':self.dvector.name, 'type':'HELLO'}))
        msg = self.parse(self.recv())
        self.node_name = msg.get('from', None)
        msg_type = msg.get('type', None)
        if not self.node_name or not msg_type:
            logger.error("Received msg coudn't be parsed")
            exit()
        if msg_type.upper() != 'WELCOME':
            logger.error("Received msg wasn't Type:WELCOME, as protocol establish")
            exit()
        
        self.dvector.connection_established(self.node_name, False)
            
class ServerWorker(Worker):
    
    def __init__(self, sckt, address, dvector):
#        retry = 3
        self.dvector = dvector
        super().__init__(sckt, address)
    
    def start(self):
        logger.info('Connected by: %s' % self.address[0])
        
        msg = self.parse(self.recv())
        self.node_name = msg.get('from', None)
        msg_type = msg.get('type', None)
        if not self.node_name or not msg_type:
            logger.error("Received msg coudn't be parsed")
            exit()
        if msg_type.upper() != 'HELLO':
            logger.error("Received msg wasn't Type:HELLO, as protocol establish")
            exit()
        answer = self.render({'from':self.dvector.name, 'type':'WELCOME'})
        self.send(answer)
        
        self.dvector.connection_established(self.node_name, True)
        
        
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
            
#            self.retry=3
#            splitted = self.data.split("~")
#            type = splitted[1].split(":")[1]
#            if(type=="DV"):
#                nodes = []
#                for i in range(2,len(splitted)):
#                    node = splitted[i].split(":")
#                    nodes.push([node[0],int(node[1])])
#                self.dvector.update(self.name,nodes)
#            elif(type=="KeepAlive"):
#                retry=3
#            
#            else:
#                retry -= 1
#            if retry == 0:
#                exit()

            time.sleep(30) 
            
#    def recv(self):
#        chunks = []
#        bytes_rcvd = 0
#        while True:
#            chunk = self.socket.recv(1024).decode('ascii')
#            if chunk == '':
#                raise RuntimeError("Socket connection broken")
#            chunks.append(chunk)
#            bytes_rcvd += len(chunk)
#            msg = self.iseof(chunks)
#            if len(msg):
#                self.data = msg
#                msg = ''