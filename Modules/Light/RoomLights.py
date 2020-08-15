from Deck.Button import Button
from Deck.Module import Module

from Connectors.HueConnector import *

class RoomLights(Module):
    def __init__(self):
        super().__init__()
        
        self._hue = HueConnector("192.168.0.55")
        
        self.set_button(0, 0, SetLightPresetButton("Room\nbright",  self._hue, CONFIG_ROOM_BRIGHT))
        self.set_button(0, 1, SetLightPresetButton("Backgr\ncolor", self._hue, CONFIG_BG_COLOR))
        self.set_button(0, 2, SetLightPresetButton("Room\ndimmed",  self._hue, CONFIG_ROOM_DIMMED))
        self.set_button(1, 0, SetLightPresetButton("Bkgnd\noff",    self._hue, CONFIG_FACE_OFF))
        self.set_button(1, 1, SetLightPresetButton("Bkgnd\ncolor",  self._hue, CONFIG_FACE_COLOR))

class SetLightPresetButton(Button):
    def __init__(self, display_name, hue, config):
        super().__init__(display_name, bg_color = "#222222")
        self._config = config
        self._hue = hue
    
    def pressed(self):
        try:
            self._hue.apply_config(self._config)
        except PhueException as e:
            print("Phue exception")

class SetLightRandomColorButton(Button):
    def __init__(self, display_name, hue):
        super().__init__(display_name)
        self._hue = hue
    
    def pressed(self):
        try:
            config = [
                (L4+R2, LightOffPreset()),
                (L1+L2+L3, LightColorPreset(hue = random.random())),
                (R1+R3+R4, LightColorPreset(hue = random.random()))
            ]
            self._hue.apply_config(config)
        except PhueException as e:
            print("Phue exception")

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
