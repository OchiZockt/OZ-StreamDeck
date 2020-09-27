from Deck.Module import Module

from Modules.OBS.TimestampManager import TimestampManager

from Modules.OBS.SceneSwitcher import SceneSwitcher
from Modules.OBS.RecordControls import RecordControls
from Modules.OBS.MarkerControls import MarkerControls
from Modules.Music.MusicControls import MusicControls

class OBS(Module):
    def __init__(self):
        super().__init__()
        
        self._timestamp_manager = TimestampManager("/tmp")
        
        self.add_module(0, 0, SceneSwitcher())
        self.add_module(3, 0, MarkerControls(self._timestamp_manager))
        self.add_module(3, 3, RecordControls(self._timestamp_manager))
        self.add_module(0, 4, MusicControls())
