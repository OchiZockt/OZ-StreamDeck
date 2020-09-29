from functools import partial

from Deck.Button import Button
from Deck.Module import Module

from Messages.Audio import *

class VolumeControl(Module):
    def __init__(self, track_number, track_name, volume):
        super().__init__()
        
        self._blink_state = False
        self._volume = volume
        
        self.set_button(0, 0, VolumeControlButton(self, track_number, "+",  1))
        self.set_button(1, 0, VolumeDisplayButton(track_number, track_name, volume))
        self.set_button(2, 0, VolumeControlButton(self, track_number, "-", -1))
        self.set_button(3, 0, MuteButton(track_number, track_name))
    
    def tick(self):
        self._blink_state = not self._blink_state
        super().tick()

class VolumeControlButton(Button):
    def __init__(self, control, track_number, display_name, volume_delta, bg_color = "#000000"):
        super().__init__(display_name, bg_color = bg_color, font_size = 36)
        self._control = control
        self._track_number = track_number
        self._volume_delta = volume_delta
    
    def pressed(self):
        self._control._volume += self._volume_delta
        self.send_to_backend(VolumeMessage(self._track_number, self._control._volume))

class VolumeDisplayButton(Button):
    def __init__(self, track_number, track_name, volume, bg_color = "#000000"):
        super().__init__(str(volume), bg_color = bg_color, font_size = 20)
        self._track_number = track_number
        self._track_name = track_name
        self._volume = volume
    
    def recv(self, msg):
        if isinstance(msg, VolumeMessage):
            if msg.track == self._track_number:
                self._volume = msg.volume
                self.set_dirty()
    
    def text(self):
        return self._track_name + "\n" + str(self._volume)

class MuteButton(Button):
    def __init__(self, track_number, track_name):
        self._unmuted_name = "Mute\n" + track_name
        self._muted_name = track_name + "\nmuted"
        self._muted = False
        self._track_number = track_number
        self._blink_state = False
        super().__init__(self._unmuted_name, font_size = 20)
    
    def recv(self, msg):
        if isinstance(msg, MuteMessage):
            if msg.track == self._track_number:
                self._muted = msg.muted
                self.set_dirty()
    
    def text(self):
        if self._muted:
            return self._muted_name
        else:
            return self._unmuted_name
    
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
    
    def pressed(self):
        self.send_to_backend(MuteMessage(self._track_number, not self._muted))
    
    def dirty(self):
        # TODO: Only refresh if necessary
        return True
