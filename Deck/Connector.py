from Messages.Common import *

class Connector:
    def __init__(self, backend):
        self._backend = backend
    
    def send_to_frontend(self, msg):
        self._backend.route(FRONTEND, msg)

    def recv(self, msg):
        pass
    
    def stop(self):
        pass
