from Deck.Button import Button
from Deck.Module import Module

from Messages.OBS import *

class SceneSwitcher(Module):
    def __init__(self, timestamp_manager):
        super().__init__(bg_color = "#111111")
        self._timestamp_manager = timestamp_manager
        
        self._sbs = False
        
        bg = "#440000"
        self.set_button(0, 0, SceneSwitchButton(self, "Start",      "Screen Start",     bg))
        self.set_button(0, 1, SceneSwitchButton(self, "Break",      "Screen Break",     bg))
        self.set_button(0, 2, SceneSwitchButton(self, "End",        "Screen End",       bg))
        
        bg = "#004400"
        self.set_button(1, 0, SceneSwitchButton(self, "Cam",        "Cam A",       bg))
        self.set_button(1, 1, SceneSwitchButton(self, "Cam+\nGame", "Cam A + Game A",  bg))
        self.set_button(1, 2, SceneSwitchButton(self, "Room\nCam",  "Cam Room",  bg))
        
        bg = "#000044"
        self.set_button(2, 0, SceneSwitchButton(self, "Game\n+Cam", "Game A + Cam A",  bg, True))
        self.set_button(2, 1, SceneSwitchButton(self, "Game",       "Game A",      bg, True))
        self.set_button(2, 2, SceneSwitchButton(self, "Game\nonly", "Game A only", bg))
        
        #self.set_button(3, 2, SBSToggleButton(self))
        self.set_button(3, 2, ABToggleButton(self))

class SceneSwitchButton(Button):
    def __init__(self, module, display_name, scene_name, bg_color, has_sbs_variant = False):
        super().__init__(text = display_name, bg_color = bg_color)
        self._module = module
        self._scene_name = scene_name
        self._has_sbs_variant = has_sbs_variant
        self._scene_selected = False
    
    def border_size(self):
        return 10 if self._scene_selected else 0
    
    def pressed(self):
        scene_name = self._scene_name
        if self._module._sbs and self._has_sbs_variant:
            scene_name = scene_name + " SBS"
        self.send_to_backend(SwitchSceneCommand(scene_name))
        self._module._timestamp_manager.mark_all(scene_name)
    
    def recv(self, msg):
        if isinstance(msg, SwitchSceneCommand):
            self._scene_selected = msg.scene_name == self._scene_name
            self.set_dirty()

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

class ABToggleButton(Button):
    def __init__(self, module):
        super().__init__()
        self._module = module
    
    def text(self):
        return "A/B"
    
    def pressed(self):
        self.send_to_backend(SwitchABCommand())
