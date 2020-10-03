from Deck.Module import Module

from Modules.SceneSwitcher import SceneSwitcher
from Modules.MusicControls import MusicControls
from Modules.LightControls import LightControls
from Modules.RecordControls import RecordControls
from Modules.MarkerControls import MarkerControls
from Modules.VolumeControls import VolumeControls

from Utils.TimestampManager import TimestampManager

class Primary(Module):
    def __init__(self):
        super().__init__()
        
        self._timestamp_manager = TimestampManager("/mnt/rec")
        
        self.add_module(0, 0, SceneSwitcher(self._timestamp_manager))
        self.add_module(0, 4, MusicControls())
        self.add_module(2, 4, LightControls())
        self.add_module(0, 3, RecordControls(self._timestamp_manager))
        self.add_module(3, 0, MarkerControls(self._timestamp_manager))
        self.add_module(1, 6, VolumeControls())
