from Connectors.OBSConnector import OBSConnector
from Connectors.OSCConnector import OSCConnector
from Connectors.HueConnector import HueConnector
from Connectors.LegConnector import LegConnector

class Backend:
    def __init__(self, frontend):
        self._frontend = frontend
        
        self._obs_streaming = OBSConnector(self, "stream", "127.0.0.1", 4444)
        self._obs_recording = OBSConnector(self, "record", "127.0.0.1", 4445)
        
        self._osc = OSCConnector(self, "127.0.0.1", 8000)
        
        self._hue = HueConnector(self, "192.168.0.55")
        
        self._leg_l = LegConnector(self, "left", "192.168.0.64")
        self._leg_r = LegConnector(self, "right", "192.168.0.63")
    
    def recv_from_frontend(self, msg):
        self._obs_streaming.recv(msg)
        self._obs_recording.recv(msg)
        
        self._osc.recv(msg)
        
        self._hue.recv(msg)
        
        self._leg_l.recv(msg)
        self._leg_r.recv(msg)
    
    def recv_from_backend(self, msg):
        self._frontend.recv_from_backend(msg)
    
    def stop(self):
        self._osc.stop()
