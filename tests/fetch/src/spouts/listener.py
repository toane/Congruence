from itertools import cycle

from streamparse import Spout


import socket

class SocketListener:
    
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.socket.listen()
        self.socket.settimeout(5)

    def __del__(self):
        self.socket.close()

class ListenSpout(Spout):
    outputs = ['word']

    def initialize(self, stormconf, context):
        #with SocketListener(15555) as s:
        #self.listener = s

        self.listener = SocketListener(15556)
    def next_tuple(self):
        try:
            conn, addr = self.listener.socket.accept()
            with conn:
                self.logger.info('Connected by {}'.format(addr))
                
                data = conn.recv(1024)
                self.logger.info('received {}'.format(data))
                self.emit([data])
                        
        except OSError:
            #self.logger.info("timed out")
            pass
