from Deck.Button import Button
from Deck.Module import Module

from Connectors.OSCConnector import OSCConnector

class VolumeControl(Module):
    def __init__(self, track_number, track_name, volume):
        super().__init__()
        
        self._blink_state = False
        self._volume = volume
        
        osc = OSCConnector("localhost", 8000)
        
        self.set_button(0, 0, VolumeControlButton(osc, track_number, "+",  1))
        self.set_button(1, 0, VolumeDisplayButton(osc, track_number))
        self.set_button(2, 0, VolumeControlButton(osc, track_number, "-", -1))
        self.set_button(3, 0, MuteButton(osc, track_number, track_name))
    
    def refresh_volume_display(self):
        self.button(1, 0).refresh()
    
    def tick(self):
        self._blink_state = not self._blink_state
        super().tick()

class VolumeControlButton(Button):
    def __init__(self, osc, track_number, display_name, volume_delta, bg_color = "#000000"):
        super().__init__(display_name, bg_color = bg_color, font_size = 36)
        self._osc = osc
        self._track_number = track_number
        self._volume_delta = volume_delta
    
    def pressed(self):
        self._parent._volume = self._parent._volume + self._volume_delta
        self._osc.set_volume(self._track_number, self._parent._volume)
        self._parent.refresh_volume_display()

class VolumeDisplayButton(Button):
    def __init__(self, osc, track_number, bg_color = "#000000"):
        super().__init__("?", bg_color = bg_color, font_size = 20)
        self._osc = osc
        self._track_number = track_number
    
    def text(self):
        return str(self._parent._volume)
    
    def refresh(self):
        self.request_refresh()

class MuteButton(Button):
    def __init__(self, osc, track_number, track_name):
        self._unmuted_name = "Mute\n" + track_name
        self._muted_name = track_name + "\nmuted"
        self._muted = False
        self._track_number = track_number
        self._osc = osc
        self._blink_state = False
        super().__init__(self._unmuted_name, font_size = 20)
    
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
        self._osc.set_muted(self._track_number, self._muted)
        self.request_refresh()
    
    def tick(self):
        if self._muted:
            self.request_refresh()
