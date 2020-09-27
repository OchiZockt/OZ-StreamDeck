from functools import partial

from Deck.Button import Button
from Deck.Module import Module

from Messages.Audio import *

class VolumeControl(Module):
    def __init__(self, track_number, track_name, volume):
        super().__init__()
        
        self._blink_state = False
        self._volume = 0
        
        self.set_button(0, 0, VolumeControlButton(track_number, "+",  1))
        self.set_button(1, 0, VolumeDisplayButton(track_number))
        self.set_button(2, 0, VolumeControlButton(track_number, "-", -1))
        self.set_button(3, 0, MuteButton(track_number, track_name))
    
    def osc_volume_callback(self, volume):
        self._volume = volume
        self.refresh_volume_display()
    
    def refresh_volume_display(self):
        self.button(1, 0).refresh()
    
    def tick(self):
        self._blink_state = not self._blink_state
        super().tick()

class VolumeControlButton(Button):
    def __init__(self, track_number, display_name, volume_delta, bg_color = "#000000"):
        super().__init__(display_name, bg_color = bg_color, font_size = 36)
        self._track_number = track_number
        self._volume_delta = volume_delta
    
    def pressed(self):
        print("Todo: Send set volume command")

class VolumeDisplayButton(Button):
    def __init__(self, track_number, bg_color = "#000000"):
        super().__init__("?", bg_color = bg_color, font_size = 20)
        self._track_number = track_number
        self._volume = "?"
    
    def osc_volume_callback(self, volume):
        self._volume = volume
    
    def text(self):
        return str(self._volume)
    
    def tick(self):
        self.request_refresh()
    
    def refresh(self):
        self.request_refresh()

class MuteButton(Button):
    def __init__(self, track_number, track_name):
        self._unmuted_name = "Mute\n" + track_name
        self._muted_name = track_name + "\nmuted"
        self._muted = False
        self._track_number = track_number
        self._blink_state = False
        super().__init__(self._unmuted_name, font_size = 20)
    
    def osc_mute_callback(self, muted):
        self._muted = muted
    
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
        self._muted = not self._muted
        self.send(SetMuteCommand(self._track_number, self._muted))
        self.request_refresh()
    
    def tick(self):
        # TODO: Only refresh if necessary.
        self.request_refresh()
