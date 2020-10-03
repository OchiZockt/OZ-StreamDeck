from Deck.Module import Module
from Deck.Button import Button

from Messages.OBS import *

class MarkerControls(Module):
    def __init__(self, timestamp_manager):
        super().__init__()
        
        self.set_button(0, 0, MarkButton(timestamp_manager))
        self.set_button(0, 1, SplitButton(timestamp_manager))

class _MarkerButtonBase(Button):
    def __init__(self, timestamp_manager):
        super().__init__(text = self.NAME, bg_color = "#990000")
        self._timestamp_manager = timestamp_manager
    
    def pressed(self):
        self._timestamp_manager.mark_all(self.NAME)

class MarkButton(_MarkerButtonBase):
    NAME = "Mark"

class SplitButton(_MarkerButtonBase):
    NAME = "Split"
    
    def pressed(self):
        super().pressed()
        self.send_to_frontend(SplitCommand())
