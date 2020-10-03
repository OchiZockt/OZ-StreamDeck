from Deck.Button import Button
from Deck.Module import Module

from Messages.OBS import *

class SceneSwitcher(Module):
    def __init__(self, timestamp_manager):
        super().__init__(bg_color = "#111111")
        self._timestamp_manager = timestamp_manager
        
        self._sbs = False
        
        bg = "#440000"
        self.set_button(0, 0, SceneSwitchButton(self, "Start",      "Start",     bg))
        self.set_button(0, 1, SceneSwitchButton(self, "Break",      "Break",     bg))
        self.set_button(0, 2, SceneSwitchButton(self, "End",        "End",       bg))
        
        bg = "#004400"
        self.set_button(1, 0, SceneSwitchButton(self, "Cam",        "Cam",       bg))
        self.set_button(1, 1, SceneSwitchButton(self, "Cam+\nGame", "Cam+Game",  bg))
        self.set_button(1, 2, SceneSwitchButton(self, "Room\nCam",  "Room Cam",  bg))
        
        bg = "#000044"
        self.set_button(2, 0, SceneSwitchButton(self, "Game\n+Cam", "Game+Cam",  bg, True))
        self.set_button(2, 1, SceneSwitchButton(self, "Game",       "Game",      bg, True))
        self.set_button(2, 2, SceneSwitchButton(self, "Game\nonly", "Game only", bg))
        
        self.set_button(3, 2, SBSToggleButton(self))

class SceneSwitchButton(Button):
    def __init__(self, module, display_name, scene_name, bg_color, has_sbs_variant = False):
        super().__init__(text = display_name, bg_color = bg_color)
        self._module = module
        self._scene_name = scene_name
        self._has_sbs_variant = has_sbs_variant
    
    def pressed(self):
        scene_name = self._scene_name
        if self._module._sbs and self._has_sbs_variant:
            scene_name = scene_name + " SBS"
        self.send_to_backend(SwitchSceneCommand(scene_name))
        self._module._timestamp_manager.mark_all(scene_name)

class SBSToggleButton(Button):
    def __init__(self, module):
        super().__init__()
        self._module = module
    
    def text(self):
        if self._module._sbs:
            return "SBS is\non"
        else:
            return "SBS is\noff"
    
    def fg_color(self):
        if self._module._sbs:
            return "#00AA00"
        else:
            return "#0000EE"
    
    def pressed(self):
        self._module._sbs = not self._module._sbs
