import socket, threading

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
            if self.iseof(chunks):
                break
        msg = ''.join(chunks)
        return msg
    
    def iseof(self, chunks):
        msg = ''.join(chunks).strip()
        if msg[-3:] == 'EOF':
            return True
        return False
        
    
    def start(self):
        # this method should be overriden
        print('Connected by:', self.address)
        while True:
            data = self.recv()
            print('Received %d bytes' % len(data))
            self.send(data)
        
class Wendy:
    
    worker_class = Worker
    
    def __init__(self, port=9080, local=False):
        self.serversocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        if local:
            self.serversocket.bind(('localhost', port))
        else:
            self.serversocket.bind((socket.gethostname(), port))
        
    def listen(self, backlog=5):
        self.serversocket.listen(backlog)
        i = 0
        while True:
            # blocking line:
            client = self.serversocket.accept()
            worker = self.worker_class(*client)
            thrd = threading.Thread(name='Thread-'+str(i), target=worker.start)
            thrd.start()
            i += 1