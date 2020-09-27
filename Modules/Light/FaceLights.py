from Deck.Button import Button
from Deck.Module import Module

from Messages.FaceLights import *

class FaceLights(Module):
    def __init__(self):
        super().__init__()
        
        self.set_button(0, 0, FaceLightButton("Face\nhigh",   3, 7, 3200, 3200))
        self.set_button(0, 1, FaceLightButton("Face\nnormal", 3, 6, 3200, 3200))
        self.set_button(0, 2, FaceLightButton("Face\noff",    0, 0, 3200, 3200))

class FaceLightButton(Button):
    def __init__(self, display_name, lb = 0, rb = 0, lc = 3500, rc = 3500):
        super().__init__(display_name)
        self.lb = lb
        self.rb = rb
        self.lc = lc
        self.rc = rc
    
    def pressed(self):
        self.send_to_backend(SetFaceLightCommand(
            self.lb > 0, self.lb, self.lc,
            self.rb > 0, self.rb, self.rc
        ))
