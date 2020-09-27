from Messages.FaceLights import *

from leglight import LegLight

class LegConnector:
    def __init__(self, backend, side, ip):
        self._backend = backend
        self._side = side
        try:
            self.leglight = LegLight(ip, 9123)
            print(self.leglight)
        except:
            print(f"LegLight connection to {ip} failed.")
    
    def send(self, msg):
        self._backend.recv_from_backend(msg)
    
    def recv(self, msg):
        if not isinstance(msg, FaceLightsMessage):
            return
        
        if isinstance(msg, SetFaceLightCommand):
            if self._side == "left":
                self.set(msg.left.on, msg.left.brightness, msg.left.color)
            elif self._side == "right":
                self.set(msg.right.on, msg.right.brightness, msg.right.color)
    
    def set(self, on, brightness = 100, color = 3500):
        if on:
            self.leglight.on()
            self.leglight.brightness(brightness)
            self.leglight.color(color)
        else:
            self.leglight.off()
