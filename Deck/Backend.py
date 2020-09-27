from Connectors.OBSConnector import OBSConnector
from Connectors.OSCConnector import OSCConnector
from Connectors.HueConnector import HueConnector
from Connectors.LegConnector import LegConnector
from Connectors.MPRISConnector import MPRISConnector

from Messages.Common import *

class Backend:
    def __init__(self, manager):
        self._manager = manager
        
        self._connectors = [
            OBSConnector(self, "stream", "127.0.0.1", 4444),
            OBSConnector(self, "record", "127.0.0.1", 4445),
            OSCConnector(self, "127.0.0.1", 8000),
            HueConnector(self, "192.168.0.55"),
            LegConnector(self, "left", "192.168.0.64"),
            LegConnector(self, "right", "192.168.0.63"),
            MPRISConnector(self)
        ]
        
    def route(self, target, msg):
        if target == BACKEND:
            for connector in self._connectors:
                connector.recv(msg)
        
        elif target == FRONTEND:
            self._manager.route(target, msg)
    
    def stop(self):
        for connector in self._connectors:
            connector.stop()
