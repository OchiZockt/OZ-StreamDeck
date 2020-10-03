from Deck.Module import Module
from Deck.Button import Button

class Checklist(Module):
    def __init__(self):
        super().__init__()
        
        checklist = [
            "Head-\nphones",
            "Cam on,\nSet zoom",
            "Turn off\nA/V recv.",
            "Turn on\nFocusrite",
            "HDMI\nSwitch",
            "Clean-up\nRec SSD",
            "Twitch\nmetadata",
            "",
            
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            
            "oz-\nmodmic",
            "Switch\nmic",
            "Check\naudio",
            "Turn mic\naway",
            "VNC\nserver",
            "oz-vnc-\nclient",
            "SteamVR",
            "OVR\nToolkit",
            
            "Borderless\nGaming",
            "Hide\npointer",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        
        COLS = 8
        
        i = 0
        for item in checklist:
            self.set_button(i // COLS, i % COLS, ChecklistButton(item))
            i = i + 1
        
        self.set_button(3, 7, DoneButton())

class ChecklistButton(Button):
    def __init__(self, text):
        super().__init__(text = text, font_size = 16)
        self._checked = False
    
    def pressed(self):
        self._checked = not self._checked
    
    def fg_color(self):
        return "#333333" if self._checked else "white"

class DoneButton(Button):
    def __init__(self):
        super().__init__("Done", bg_color = "darkgreen")
    
    def pressed(self):
        self._parent.set_enabled(False)
        self.request_layout_rebuild()
