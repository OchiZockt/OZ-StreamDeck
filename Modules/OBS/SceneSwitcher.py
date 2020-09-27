from Deck.Button import Button
from Deck.Module import Module

from Messages.OBS import *

class SceneSwitcher(Module):
    def __init__(self):
        super().__init__(bg_color = "#111111")
        
        self._sbs = False
        
        self.set_button(0, 0, SceneSwitchButton(self, "Start",      bg_color = "#440000"))
        self.set_button(0, 1, SceneSwitchButton(self, "Break",      bg_color = "#440000"))
        self.set_button(0, 2, SceneSwitchButton(self, "End",        bg_color = "#440000"))
        
        self.set_button(1, 0, SceneSwitchButton(self, "Cam",        bg_color = "#004400"))
        self.set_button(1, 1, SceneSwitchButton(self, "Cam+\nGame", bg_color = "#004400"))
        
        self.set_button(2, 0, SceneSwitchButton(self, "Game\n+Cam", bg_color = "#000044"))
        self.set_button(2, 1, SceneSwitchButton(self, "Game",       bg_color = "#000044"))
        self.set_button(2, 2, SceneSwitchButton(self, "Game\nonly", bg_color = "#000044"))
        
        self.set_button(1, 2, SBSToggleButton(self))

class SceneSwitchButton(Button):
    def __init__(self, module, display_name, scene_name = None, bg_color = None):
        super().__init__(text = display_name, bg_color = bg_color)
        self._module = module
        
        if scene_name is None:
            self._scene_name = display_name.replace("\n", "")
        else:
            self._scene_name = scene_name
    
    def pressed(self):
        scene_name = self._scene_name
        if self._module._sbs and (scene_name == "Game+Cam" or scene_name == "Game"):
            scene_name = scene_name + " SBS"
        self.send_to_backend(SwitchSceneCommand(scene_name))

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
        self.request_refresh()
