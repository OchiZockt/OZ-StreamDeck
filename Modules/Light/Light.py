from Deck.Module import Module

from Modules.Light.RoomLights import RoomLights
from Modules.Light.FaceLights import FaceLights

class Light(Module):
    def __init__(self):
        super().__init__()
        
        self.add_module(0, 0, RoomLights())
        self.add_module(0, 4, FaceLights())
