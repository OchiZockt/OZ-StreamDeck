from Deck.Module import Module
from Deck.Button import Button

from Messages.FaceLights import *
from Messages.RoomLights import *
from Connectors.HueConnector import *

class LightControls(Module):
    def __init__(self):
        super().__init__(bg_color = "#001e42")
        
        self.set_button(0, 0, LightButton("Light\nColor",   3, 6, 3200, 3200, CONFIG_BG_COLOR))
        self.set_button(0, 1, LightButton("Light\nDimmed",  3, 6, 3200, 3200, CONFIG_ROOM_DIMMED))
        self.set_button(1, 0, LightButton("Light\nEnd",     0, 0, 3200, 3200, CONFIG_BG_COLOR))
        self.set_button(1, 1, LightButton("Light\nNormal",  0, 0, 3200, 3200, CONFIG_ROOM_BRIGHT))
        
class LightButton(Button):
    def __init__(self, text, face_lb, face_rb, face_lc, face_rc, room_config):
        super().__init__(text = text)
        
        self._face_lb = face_lb
        self._face_rb = face_rb
        self._face_lc = face_lc
        self._face_rc = face_rc
        self._room_config = room_config
    
    def pressed(self):
        try:
            self.send_to_backend(SetPresetCommand(self._room_config))
        except PhueException as e:
            print("Phue exception")
        
        self.send_to_backend(SetFaceLightCommand(
            self._face_lb > 0, self._face_lb, self._face_lc,
            self._face_rb > 0, self._face_rb, self._face_rc
        ))

# Hue color configs

HUE_RED     = 0.0 / 6.0
HUE_YELLOW  = 1.0 / 6.0
HUE_GREEN   = 2.0 / 6.0
HUE_CYAN    = 3.0 / 6.0
HUE_BLUE    = 4.0 / 6.0
HUE_PURPLE  = 5.0 / 6.0

FACE_L  = ["Face L"]
FACE_R  = ["Face R"]
L1      = ["L1"]
L2      = ["L2"]
L3      = ["L3"]
L4      = ["L4"]
R1      = ["R1"]
R2      = ["R2"]
R3      = ["R3"]
R4      = ["R4"]

ROOM_WHITE_TEMP = 0.55

CONFIG_ROOM_BRIGHT = [
    (FACE_L, LightOffPreset()),
    (FACE_R, LightOffPreset()),
    (L1+L2+L3+L4+R1+R2+R3+R4, LightTempPreset(temp = ROOM_WHITE_TEMP))
]

CONFIG_ROOM_DIMMED = [
    (FACE_L, LightOffPreset()),
    (FACE_R, LightOffPreset()),
    (L1+L2+L3+L4+R1+R2+R3+R4, LightTempPreset(bri = 0.5, temp = ROOM_WHITE_TEMP))
]

CONFIG_ROOM_OFF = [
    (FACE_L+FACE_R+L1+L2+L3+L4+R1+R2+R3+R4, LightOffPreset())
]

CONFIG_BG_NORMAL = [
    (L4+R2, LightOffPreset()),
    (L1+L2+L3+R1+R3+R4, LightTempPreset(bri = 0.4, temp = ROOM_WHITE_TEMP))
]

CONFIG_BG_DIMMED = [
    (L4+R2, LightOffPreset()),
    (L1+L2+L3+R1+R3+R4, LightTempPreset(bri = 0.2, temp = ROOM_WHITE_TEMP))
]

#CONFIG_BG_COLOR = [
#    (L4+R2, LightOffPreset()),
#    (L1+L2+L3, LightColorPreset(hue = HUE_RED)),
#    (R1+R3+R4, LightColorPreset(hue = HUE_BLUE, bri = 0.5))
#]

CONFIG_BG_COLOR = [
    (L4+R2, LightOffPreset()),
    (L2+L3, LightColorPreset(hue = HUE_RED,  sat = 1.0)),
    (R4, LightColorPreset(hue = HUE_BLUE, sat = 1.0, bri = 0.5)),
    (R3, LightColorPreset(hue = HUE_BLUE, sat = 1.0, bri = 1.0)),
    (L1+R1, LightTempPreset(bri = 0.2, temp = ROOM_WHITE_TEMP))
]

CONFIG_BG_COLOR_2 = [
    (L4+R2, LightOffPreset()),
    (R3+R4, LightColorPreset(hue = HUE_RED,  sat = 1.0)),
    (L2, LightColorPreset(hue = HUE_BLUE, sat = 1.0, bri = 1.0)),
    (L3, LightColorPreset(hue = HUE_BLUE, sat = 1.0, bri = 0.5)),
    (L1+R1, LightTempPreset(bri = 0.2, temp = ROOM_WHITE_TEMP))
]

CONFIG_BG_OFF = [
    (L1+L2+L3+L4+R1+R2+R3+R4, LightOffPreset())
]

CONFIG_FACE_NORMAL = [
    (FACE_L, LightTempPreset(bri = 0.25, temp = ROOM_WHITE_TEMP)),
    (FACE_R, LightTempPreset(bri = 0.6, temp = ROOM_WHITE_TEMP))
]

CONFIG_FACE_DIMMED = [
    (FACE_L, LightTempPreset(bri = 0.2, temp = ROOM_WHITE_TEMP)),
    (FACE_R, LightTempPreset(bri = 0.5, temp = ROOM_WHITE_TEMP))
]

CONFIG_FACE_COLOR = [
    (FACE_L, LightColorPreset(hue = HUE_BLUE)),
    (FACE_R, LightColorPreset(hue = HUE_RED))
]

CONFIG_FACE_OFF = [
    (FACE_L+FACE_R, LightOffPreset())
]
