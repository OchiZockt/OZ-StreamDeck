from subprocess import call

from Deck.Module import Module
from Deck.Button import Button

class DiscordControls(Module):
    def __init__(self):
        super().__init__()
        
        self.set_button(0, 0, DiscordMuteToggleButton())

class DiscordMuteToggleButton(Button):
    def __init__(self):
        super().__init__("Discord\nmute", bg_color = "#4b0100")
    
    def pressed(self):
        call(["xte", "key Pause"])
