from Deck.Button import Button
from Deck.Module import Module

from Connectors.OBSConnector import OBSConnector

class SceneSwitcher(Module):
    def __init__(self, obs_stream):
        super().__init__(bg_color = "#111111")
        
        self.set_button(0, 0, SceneSwitchButton(obs_stream, "Start"))
        self.set_button(0, 1, SceneSwitchButton(obs_stream, "Break"))
        self.set_button(0, 2, SceneSwitchButton(obs_stream, "End"))
        
        self.set_button(1, 0, SceneSwitchButton(obs_stream, "Cam"))
        self.set_button(1, 1, SceneSwitchButton(obs_stream, "Game\n+Cam"))
        self.set_button(1, 2, SceneSwitchButton(obs_stream, "Game"))
        
        self.set_button(2, 0, SceneSwitchButton(obs_stream, "Game\nonly"))
        self.set_button(2, 1, SceneSwitchButton(obs_stream, "Cam+\nGame"))

class SceneSwitchButton(Button):
    def __init__(self, obs_stream, display_name, scene_name = None):
        super().__init__(text = display_name)
        
        self._obs = obs_stream
        
        if scene_name is None:
            self._scene_name = display_name.replace("\n", "")
        else:
            self._scene_name = scene_name
    
    def pressed(self):
        self._obs.switch_scene(self._scene_name)
