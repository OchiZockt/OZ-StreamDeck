from Deck.Module import Module
from Deck.Button import Button

NONE = 0
RECORD = 1
STREAM = 2

class RecordControls(Module):
    def __init__(self, timestamp_manager, obs_stream, obs_record):
        super().__init__()
        
        self.set_button(0, 0, TimestampButton(timestamp_manager, STREAM, obs_stream, "Stream"))
        self.set_button(1, 0, TimestampButton(timestamp_manager, RECORD, obs_stream, "StrRec"))
        self.set_button(2, 0, TimestampButton(timestamp_manager, RECORD, obs_record, "Record"))
        self.set_button(3, 0, TimestampButton(timestamp_manager, NONE, None, "Episode"))

class TimestampButton(Button):
    def __init__(self, timestamp_manager, kind, obs, display_name):
        super().__init__()
        
        self._display_name = display_name
        self._ts = timestamp_manager.get(self._display_name)
        self._kind = kind
        self._obs = obs
    
    def text(self):
        return self._display_name + "\n" + self._ts.for_display()
    
    def pressed(self):
        if self._kind == NONE:
            return
        
        self._ts.toggle_running()
        if self._kind == RECORD:
            self._obs.set_recording(self._ts.running())
        elif self._kins == STREAM:
            self._obs.set_streaming(self._ts.running())
        
        self.request_refresh()

    def tick(self):
        if self._ts.running():
            self.request_refresh()
