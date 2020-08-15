from Deck.Button import Button
from Deck.Module import Module

from Connectors.LegConnector import *

class FaceLights(Module):
    def __init__(self):
        super().__init__()
        
        self._leg_l = LegConnector("192.168.0.64")
        self._leg_r = LegConnector("192.168.0.63")
        
        self.set_button(0, 0, FaceLightButton("Face\nhigh",   self._leg_l, self._leg_r, 3, 7, 3200, 3200))
        self.set_button(0, 1, FaceLightButton("Face\nnormal", self._leg_l, self._leg_r, 3, 6, 3200, 3200))
        self.set_button(0, 2, FaceLightButton("Face\noff",    self._leg_l, self._leg_r, 0, 0, 3200, 3200))

class FaceLightButton(Button):
    def __init__(self, display_name, l_comm, r_comm, lb = 0, rb = 0, lc = 3500, rc = 3500):
        super().__init__(display_name)
        self.l_comm = l_comm
        self.r_comm = r_comm
        self.lb = lb
        self.rb = rb
        self.lc = lc
        self.rc = rc
    
    def pressed(self):
        self.l_comm.set(self.lb > 0, self.lb, self.lc)
        self.r_comm.set(self.rb > 0, self.rb, self.rc)
