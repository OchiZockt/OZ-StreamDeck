from Deck.Module import Module

from Modules.OBS.TimestampManager import TimestampManager
from Connectors.OBSConnector import OBSConnector

from Modules.OBS.SceneSwitcher import SceneSwitcher
from Modules.OBS.RecordControls import RecordControls
from Modules.OBS.MarkerControls import MarkerControls

class OBS(Module):
    def __init__(self):
        super().__init__()
        
        self._obs_stream = OBSConnector("localhost", 4444)
        self._obs_record = OBSConnector("localhost", 4445)
        
        self._timestamp_manager = TimestampManager("/tmp")
        
        self._scene_switcher = SceneSwitcher(self._obs_stream)
        self._marker_controls = MarkerControls(self._timestamp_manager)
        self._record_controls = RecordControls(self._timestamp_manager, self._obs_stream, self._obs_record)
        
        self.add_module(0, 0, self._scene_switcher)
        self.add_module(3, 0, self._marker_controls)
        self.add_module(0, 4, self._record_controls)
