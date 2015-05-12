from wendy import Wendy
from distvector import DVWorker

# example to get distance vector working:
def start():
    server = Wendy()
    server.worker_class = DVWorker
    # this blocks
    server.listen()