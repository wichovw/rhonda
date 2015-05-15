import socket, threading
from logger import logger

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
        return msg
    
    def iseof(self, chunks):
        msg = ''.join(chunks).strip()
        if '~~' in msg:
            return msg[:msg.find('~~')]
        return []
        
    
    def start(self):
        # this method should be overriden
        logger.info('Connected by: %s' % self.address[0])
        while True:
            data = self.recv()
            logger.debug('Received %d bytes' % len(data))
            self.send(data)
        
class Wendy:
    
    worker_class = Worker
    
    def __init__(self, port=9080, local=False):
        self.serversocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        host = ''
        if local:
            self.serversocket.bind(('localhost', port))
            host = 'localhost'
        else:
            self.serversocket.bind((socket.gethostname(), port))
            host = socket.gethostbyname(socket.gethostname())
        logger.info('Server binded to %s:%s' % (host, port))
        
    def listen(self, backlog=5):
        self.serversocket.listen(backlog)
        i = 0
        while True:
            # blocking line:
            client = self.serversocket.accept()
            worker = self.worker_class(*client)
            thrd = threading.Thread(name='Worker-'+str(i), target=worker.start)
            thrd.start()
            i += 1