from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher

class OSCConnector:
    def __init__(self, host, port):
        self.client = SimpleUDPClient(host, port)
    
    def set_volume(self, track_number, volume):
        self.client.send_message(f"/track/{track_number}/volume/db", volume)
    
    def set_muted(self, track_number, muted):
        self.client.send_message(f"/track/{track_number}/mute", int(muted))
