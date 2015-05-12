from wendy import Worker

class DVWorker(Worker):
    
    def __init__(self, sckt, address):
        # init things
        super().__init__(sckt, address)
    
    def start(self):
        print('Connected by:', self.address)
        while True:
            data = self.recv()
            print('Received cuz yolo %d bytes' % len(data))
            self.send(data)