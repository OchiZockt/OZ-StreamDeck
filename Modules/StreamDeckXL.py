from Deck.Module import Module

from Modules.Audio.Audio import Audio
from Modules.Checklist.Checklist import Checklist
from Modules.Light.Light import Light
from Modules.OBS.OBS import OBS

from Modules.Switcher import Switcher

class StreamDeckXL(Module):
    def __init__(self):
        super().__init__()
        
        audio_module = Audio()
        checklist_module = Checklist()
        light_module = Light()
        obs_module = OBS()
        
        self.add_module(0, 0, audio_module)
        self.add_module(0, 0, checklist_module)
        self.add_module(0, 0, light_module)
        self.add_module(0, 0, obs_module)
        
        audio_module.set_enabled(False)
        checklist_module.set_enabled(False)
        light_module.set_enabled(False)
        obs_module.set_enabled(False)
        
        self.add_module(0, 7, Switcher({
            "OBS": obs_module,
            "Light": light_module,
            "Audio": audio_module,
            "Checklist": checklist_module
        }))
