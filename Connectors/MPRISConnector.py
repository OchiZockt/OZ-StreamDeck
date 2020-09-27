from subprocess import run

from Deck.Connector import Connector
from Messages.Music import *

class MPRISConnector(Connector):
    def __init__(self, backend):
        super().__init__(backend)
    
    def recv(self, msg):
        if not isinstance(msg, MusicMessage):
            return
        
        if isinstance(msg, PlayCommand):
            run(["playerctl", "play"])
        
        elif isinstance(msg, StopCommand):
            run(["playerctl", "stop"])
        
        elif isinstance(msg, PrevCommand):
            run(["playerctl", "previous"])
        
        elif isinstance(msg, NextCommand):
            run(["playerctl", "next"])
