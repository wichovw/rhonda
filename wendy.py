import socket, threading
from logger import logger
from workers import Worker, ServerWorker

class Wendy:
    
    worker_class = Worker
    kwargs = {}
    
    def __init__(self, port=1234, local=False):
        self.serversocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        self.workers = []
        host = ''
        if local:
            self.serversocket.bind(('localhost', port))
            host = 'localhost'
        else:
            self.serversocket.bind((socket.gethostname(), port))
            host = socket.gethostbyname(socket.gethostname())
        logger.info('Server bound to %s:%s' % (host, port))
        
    def listen(self, backlog=5):
        self.serversocket.listen(backlog)
        i = 0
        while True:
            # blocking line:
            client = self.serversocket.accept()
            worker = self.create_worker(client, 'Worker-%d'%i)
            self.workers.append(worker)
            i += 1
            
    def create_worker(self, client, name):
        worker = self.worker_class(*client)
        thrd = threading.Thread(name=name, target=worker.start)
        thrd.start()
        return worker
    
class DVWendy(Wendy):
    
    def __init__(self, distvector, port=9080, **kwargs):
        self.dv = distvector
        super().__init__(port=port, **kwargs)
        
    def create_worker(self, client, name):
        worker = ServerWorker(*client, dvector=self.dv)
        thrd = threading.Thread(name='Server-'+name, target=worker.start)
        thrd.start()
        return worker