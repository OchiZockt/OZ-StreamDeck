from Deck.Button import Button
from Deck.Module import Module

from Connectors.OBSConnector import OBSConnector
from Messages.OBS import *

class SceneSwitcher(Module):
    def __init__(self):
        super().__init__(bg_color = "#111111")
        
        self.set_button(0, 0, SceneSwitchButton("Start"))
        self.set_button(0, 1, SceneSwitchButton("Break"))
        self.set_button(0, 2, SceneSwitchButton("End"))
        
        self.set_button(1, 0, SceneSwitchButton("Cam"))
        self.set_button(1, 1, SceneSwitchButton("Game\n+Cam"))
        self.set_button(1, 2, SceneSwitchButton("Game"))
        
        self.set_button(2, 0, SceneSwitchButton("Game\nonly"))
        self.set_button(2, 1, SceneSwitchButton("Cam+\nGame"))

class SceneSwitchButton(Button):
    def __init__(self, display_name, scene_name = None):
        super().__init__(text = display_name)
        
        if scene_name is None:
            self._scene_name = display_name.replace("\n", "")
        else:
            self._scene_name = scene_name
    
    def pressed(self):
        self.send_to_backend(SwitchSceneCommand(self._scene_name))
