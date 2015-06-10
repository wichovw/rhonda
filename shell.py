from logger import logger

def start():
    from distvector import DistVector, config_file
    import socket, threading
    from workers import ClientWorker
    from wendy import DVWendy
    
    dvector = DistVector(config_file)
    
    def action(port, dvector):
        while True:
            try:
                sock = socket.create_connection(
                    (dvector.nodes[node].address, 9080),
                    socket.getdefaulttimeout(),
                    (socket.gethostname(), port)
                )
                worker = ClientWorker(sock, dvector.nodes[node].address, dvector)
                worker.start()
            except:
                continue
    
    port = 1234
    for node in dvector.nodes:
        t = threading.Thread(target=action, args=(port, dvector))
        t.daemon = True
        t.start()
        port += 1
        
    
    # init client workers
    # init wendy
    # init forwarding wendy
    
    server = DVWendy(dvector)
#    server.worker_class = DVWorker
#    distvector = DistVector
#    server.worker_class = DVWorker
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