#import cherrypy
#import os
#from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
#from ws4py.websocket import WebSocket
#from ws4py.messaging import TextMessage
#import random
#
#PATH = os.path.abspath(os.path.dirname(__file__))
#PATH = os.path.join(PATH, 'chat')
#
#'''
#There are two kind of messages: game (json) and viewer (space separated). All messages are broadcasted.
#'''
#class ChatSocket(WebSocket):
#    def received_message(self, m):
#        cherrypy.engine.publish('websocket-broadcast', m)
#    
#    def closed(self, code, reason="A client left the room without a proper explanation."):
#        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))
#
#class ChatServer(object):
#        
#    @cherrypy.expose
#    def index(self):
#        return open(os.path.join(PATH, 'index.html'))
#    
#    @cherrypy.expose
#    def chat(self):
#        handler = cherrypy.request.ws_handler
#            
if __name__ == '__main__':
    
#    #Set IP to current lolcal
#    from socket import gethostbyname as get_host, gethostname as get_name
#    host = get_host(get_name())
#    port = int(os.environ.get('PORT', '5000'))
#    
#    cherrypy.config.update({'server.socket_host': host})
#    cherrypy.config.update({'server.socket_port': port})
#
#    #Load server
#    WebSocketPlugin(cherrypy.engine).subscribe()
#    cherrypy.tools.websocket = WebSocketTool()
#    
#    server_config ={
#        '/': {
#            'tools.staticdir.on': True,
#            'tools.staticdir.dir': PATH
#        },
#        '/play' : {
#            'tools.websocket.on': True,
#            'tools.websocket.handler_cls': JengaGame
#        }
#    }
#    cherrypy.quickstart(ChatServer(), '/', server_config)
    
    #Now open socket
    import socket
    import threading
    
    host = 'localhost'
    port = 1992
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.bind(('localhost', port))
    chat_socket.listen(1)
    
    def read_msgs(client):
        print("Got here")
        while True:
            chunk = client.recv(1024).decode('ascii')
            print(chunk.replace("~", "\n"))
    
    #Acept connections
    while True:
        #Accept connection
        client = chat_socket.accept()
        t = threading.Thread(target=read_msgs, args = (client))
        t.deamon = True
        t.start()
        
    
    