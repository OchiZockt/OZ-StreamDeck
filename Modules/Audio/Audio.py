from Deck.Button import Button
from Deck.Module import Module

from Modules.Audio.VolumeControl import VolumeControl

class Audio(Module):
    def __init__(self):
        super().__init__()
        
        # TODO: Get the real (initial) volume from OSC
        
        self.add_module(0, 0, VolumeControl(2, "Mic", 0.0))
        self.add_module(0, 1, VolumeControl(4, "Game", -6.0))
        self.add_module(0, 2, VolumeControl(8, "Music", -18.0))
    
    def stop(self):
        print("Audio stop")
