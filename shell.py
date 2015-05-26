from wendy import Wendy
from distvector import DVWorker, DistVector
from logger import logger

# example to get distance vector working:
def start():
    server = Wendy()
    server.worker_class = DVWorker
    distvector = DistVector
    server.worker_class = DVWorker
    # this blocks
    server.listen()

if __name__ == '__main__':
    from prompt_toolkit.shortcuts import get_input
    import threading

    #Welcome message
    print("\n--------------------------------------------------\r\nRhonda: Router project \n\n Available Commands:")
    print("\tstart\n\tquit")
    print("--------------------------------------------------\n\n")

    #Start flag
    served = None

    #Console loop
    while True:
        parts = get_input('clsfy> ').lower().split()
        #Check which command
        if parts[0] == 'quit':
            break
        elif parts[0] == 'start':
            if not served:
                served = threading.Thread(target=start)
                served.daemon = True
                served.start()
        else:
            print("You can only start the router once.");
    print("Good bye! - Rhonda")