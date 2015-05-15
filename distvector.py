from wendy import Worker
import time

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

       
						