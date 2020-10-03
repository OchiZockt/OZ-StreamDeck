from Deck.Module import Module
from Deck.Button import Button

from Messages.Audio import *

class VolumeControls(Module):
    def __init__(self):
        super().__init__()
        
        self.set_button(0, 0, TrackChooserButton(self, 2, "Mic", 0.0))
        self.set_button(1, 0, TrackChooserButton(self, 4, "Game", -6.0, True))
        self.set_button(2, 0, TrackChooserButton(self, 8, "Music", -18.0))
        
        self.set_button(0, 1, VolumeButton(1))
        self.set_button(1, 1, MuteButton())
        self.set_button(2, 1, VolumeButton(-1))
        
        self._blink_state = False
    
    def tick(self):
        self._blink_state = not self._blink_state
        super().tick()

class TrackChooserButton(Button):
    def __init__(self, parent, track_number, track_name, initial_volume, initial_selected = False):
        super().__init__(border_color = "grey")
        self._parent = parent
        self._track_number = track_number
        self._track_name = track_name
        self._volume = initial_volume
        self._muted = False
        self._selected = initial_selected
    
    def pressed(self):
        self.send_to_frontend(_SelectTrackMessage(self._track_number))
    
    def recv(self, msg):
        if isinstance(msg, _SelectTrackMessage):
            self._selected = (msg.track_number == self._track_number and not self._selected)
            self.set_dirty()
        
        elif isinstance(msg, _SetVolumeMessage) and self._selected:
            self.send_to_backend(VolumeMessage(self._track_number, self._volume + msg.volume_delta))
        
        elif isinstance(msg, _ToggleMuteMessage) and self._selected:
            self.send_to_backend(MuteMessage(self._track_number, not self._muted))
        
        elif isinstance(msg, VolumeMessage):
            if msg.track == self._track_number:
                self._volume = msg.volume
                self.set_dirty()
        
        elif isinstance(msg, MuteMessage):
            if msg.track == self._track_number:
                self._muted = msg.muted
                self.set_dirty()
    
    def text(self):
        return self._track_name + "\n" + str(self._volume)
    
    def fg_color(self):
        if self._muted:
            return "#FFFF00" if self._parent._blink_state else "#FF0000"
        else:
            return "#FFFFFF"
    
    def bg_color(self):
        if self._muted:
            return "#FF0000" if self._parent._blink_state else "#FFFF00"
        else:
            return "#000000"
    
    def border_size(self):
        return 10 if self._selected else 0
    
    def dirty(self):
        return super().dirty() or self._muted

class VolumeButton(Button):
    def __init__(self, volume_delta):
        super().__init__(font_size = 28)
        self._volume_delta = volume_delta
    
    def pressed(self):
        self.send_to_frontend(_SetVolumeMessage(self._volume_delta))
    
    def text(self):
        return "+" if self._volume_delta > 0 else "-"

class MuteButton(Button):
    def __init__(self):
        super().__init__(text = "Mute")
    
    def pressed(self):
        self.send_to_frontend(_ToggleMuteMessage())

# Private

class _SelectTrackMessage:
    def __init__(self, track_number):
        self.track_number = track_number

class _SetVolumeMessage:
    def __init__(self, volume_delta):
        self.volume_delta = volume_delta

class _ToggleMuteMessage:
    def __init__(self):
        pass
