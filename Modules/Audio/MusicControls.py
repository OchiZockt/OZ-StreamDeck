from Deck.Button import Button
from Deck.Module import Module

from Messages.Music import *

class MusicControls(Module):
    def __init__(self):
        super().__init__(bg_color = "#111111")
        
        self.set_button(0, 0, PlayButton())
        self.set_button(0, 1, StopButton())
        self.set_button(1, 0, PrevButton())
        self.set_button(1, 1, NextButton())

class PlayButton(Button):
    def __init__(self):
        super().__init__(text = "Play", bg_color = "darkgreen")
    
    def pressed(self):
        self.send_to_backend(PlayCommand())

class StopButton(Button):
    def __init__(self):
        super().__init__(text = "Stop", bg_color = "darkred")
    
    def pressed(self):
        self.send_to_backend(StopCommand())

class PrevButton(Button):
    def __init__(self):
        super().__init__(text = "Prev", bg_color = "#CC5500")
    
    def pressed(self):
        self.send_to_backend(PrevCommand())

class NextButton(Button):
    def __init__(self):
        super().__init__(text = "Next", bg_color = "#CC5500")
    
    def pressed(self):
        self.send_to_backend(NextCommand())
