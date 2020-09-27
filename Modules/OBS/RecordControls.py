from Deck.Module import Module
from Deck.Button import Button

from Messages.OBS import *

NONE = 0
RECORD = 1
STREAM = 2

class RecordControls(Module):
    def __init__(self, timestamp_manager):
        super().__init__()
        
        self.set_button(0, 0, TimestampButton(timestamp_manager, STREAM, STREAM, "Stream"))
        self.set_button(0, 1, TimestampButton(timestamp_manager, STREAM, RECORD, "StrRec"))
        self.set_button(0, 2, TimestampButton(timestamp_manager, RECORD, RECORD, "Record"))
        self.set_button(0, 3, TimestampButton(timestamp_manager, NONE, NONE, "Episode"))

class TimestampButton(Button):
    def __init__(self, timestamp_manager, obs_kind, ctl_kind, display_name):
        super().__init__()
        
        self._display_name = display_name
        self._ts = timestamp_manager.get(self._display_name)
        self._obs_kind = obs_kind
        self._ctl_kind = ctl_kind
        
        if self._display_name == "Episode":
            self._ts.set_running(True)
    
    def text(self):
        return self._display_name + "\n" + self._ts.for_display()
    
    def pressed(self):
        if self._obs_kind == NONE or self._ctl_kind == NONE:
            return
        
        self._ts.toggle_running()
        if self._obs_kind == RECORD and self._ctl_kind == RECORD:
            self.send_to_backend(StartStopCommand("record", "record", self._ts.running()))
        elif self._obs_kind == STREAM and self._ctl_kind == RECORD:
            self.send_to_backend(StartStopCommand("stream", "record", self._ts.running()))
        elif self._obs_kind == STREAM and self._ctl_kind == STREAM:
            self.send_to_backend(StartStopCommand("stream", "stream", self._ts.running()))
        
        self.request_refresh()

    def recv(self, msg):
        if isinstance(msg, SplitCommand) and self._display_name == "Episode":
            self._ts.reset()
            self.request_refresh()

    def tick(self):
        if self._ts.running():
            self.request_refresh()
