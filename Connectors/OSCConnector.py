from Messages.Audio import *

import asyncio
import threading

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

class OSCConnector:
    def __init__(self, backend, host, port):
        self._backend = backend
        self.client = SimpleUDPClient(host, port)
        
        self._osc_server_lock = threading.Lock()
        dispatcher = Dispatcher()
        dispatcher.map("/track/*/volume/str", self.osc_volume_handler)
        dispatcher.map("/track/*/mute/toggle", self.osc_mute_handler)
        #dispatcher.set_default_handler(self.osc_default_handler)
        self._osc_server = BlockingOSCUDPServer(("127.0.0.1", 8001), dispatcher)
        self._osc_server_thread = threading.Thread(target = self._osc_server.serve_forever)
        self._osc_server_thread.start()
    
    def send(self, msg):
        self._backend.recv_from_backend(msg)
    
    def recv(self, msg):
        if not isinstance(msg, AudioMessage):
            return
        
        if isinstance(msg, VolumeMessage):
            self.set_volume(msg.track, msg.volume)
        
        if isinstance(msg, MuteMessage):
            self.set_muted(msg.track, msg.muted)
    
    def stop(self):
        self._osc_server.shutdown()
    
    def send_refresh_request(self):
        print("Sending refresh request to REAPER...")
        self.client.send_message("/action", 41743)
    
    def osc_default_handler(self, address, *args):
        print("OSC default handler:", address, args)
    
    def osc_volume_handler(self, address, *args):
        #print(address, args)
        with self._osc_server_lock:
            try:
                track_number = int(address.split("/")[2])
                self.send(VolumeMessage(track_number, float(args[0][:-2])))
            except:
                pass
    
    def osc_mute_handler(self, address, *args):
        with self._osc_server_lock:
            try:
                track_number = int(address.split("/")[2])
                self.send(MuteMessage(track_number, bool(args[0])))
            except:
                pass
    
    def set_volume(self, track_number, volume):
        self.client.send_message(f"/track/{track_number}/volume/db", volume)
    
    def set_muted(self, track_number, muted):
        self.client.send_message(f"/track/{track_number}/mute", int(muted))
