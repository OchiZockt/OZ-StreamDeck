from Deck.Module import Module
from Deck.Button import Button

from Messages.OBS import *

class MarkerControls(Module):
    def __init__(self, timestamp_manager):
        super().__init__()
        
        self.set_button(0, 0, MarkerButton(timestamp_manager, "Mark"))
        self.set_button(0, 1, MarkerButton(timestamp_manager, "Split"))

class MarkerButton(Button):
    def __init__(self, timestamp_manager, display_name):
        super().__init__(bg_color = "#990000")
        
        self._timestamp_manager = timestamp_manager
        self._display_name = display_name
    
    def text(self):
        return self._display_name

    def pressed(self):
        self._timestamp_manager.mark_all(self._display_name)
        self.send_to_frontend(SplitCommand())
