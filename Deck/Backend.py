from Connectors.OBSConnector import OBSConnector
from Connectors.OSCConnector import OSCConnector
from Connectors.HueConnector import HueConnector
from Connectors.LegConnector import LegConnector

from Messages.Common import *

class Backend:
    def __init__(self, manager):
        self._manager = manager
        
        self._obs_streaming = OBSConnector(self, "stream", "127.0.0.1", 4444)
        self._obs_recording = OBSConnector(self, "record", "127.0.0.1", 4445)
        
        self._osc = OSCConnector(self, "127.0.0.1", 8000)
        
        self._hue = HueConnector(self, "192.168.0.55")
        
        self._leg_l = LegConnector(self, "left", "192.168.0.64")
        self._leg_r = LegConnector(self, "right", "192.168.0.63")
    
    def route(self, target, msg):
        if target == BACKEND:
            self._obs_streaming.recv(msg)
            self._obs_recording.recv(msg)
            
            self._osc.recv(msg)
            
            self._hue.recv(msg)
            
            self._leg_l.recv(msg)
            self._leg_r.recv(msg)
        
        elif target == FRONTEND:
            self._manager.route(target, msg)
    
    def stop(self):
        self._osc.stop()
