#from pprint import pprint

from Messages.RoomLights import *

from phue import Bridge, PhueException

class LightSet:
    def __init__(self, lights):
        self._lights = lights
    
    def lights(self):
        return self._lights

class LightPreset:
    def __init__(self, bri):
        self._bri = bri
        
    def phue_dict(self):
        return {
            "on": True,
            "bri": int(254 * self._bri),
            "transitiontime": 1
        }

class LightOffPreset:
    def __init__(self):
        pass
    
    def phue_dict(self):
        return {
            "on": False,
            "transitiontime": 1
        }

class LightTempPreset(LightPreset):
    def __init__(self, bri = 1.0, temp = 0.5):
        super().__init__(bri)
        self._temp = temp
    
    def phue_dict(self):
        d = super().phue_dict()
        d.update({
            "ct": 154 + int(346 * self._temp)
        })
        return d
    
class LightColorPreset(LightPreset):
    def __init__(self, bri = 1.0, hue = 0.0, sat = 1.0):
        super().__init__(bri)
        self._hue = hue
        self._sat = sat
    
    def phue_dict(self):
        d = super().phue_dict()
        d.update({
            "hue": int(65535 * self._hue),
            "sat": int(254 * self._sat)
        })
        return d

class HueConnector:
    def __init__(self, backend, ip):
        self._backend = backend
        self.bridge = Bridge(ip)
        self.bridge.connect()
        
        api = self.bridge.get_api()
        
        self.light_indices = {}
        for idx, data in api["lights"].items():
            self.light_indices[data["name"]] = int(idx)
        
        self.group_indices = {}
        for idx, data in api["groups"].items():
            self.group_indices[data["name"]] = int(idx)
        
        #pprint(api)
    
    def send(self, msg):
        self._backend.recv_from_backend(msg)
    
    def recv(self, msg):
        if not isinstance(msg, RoomLightsMessage):
            return
        
        if isinstance(msg, SetPresetCommand):
            self.apply_config(msg.preset)
    
    def apply_config(self, config):
        for c in config:
            lights, preset = c
            for light in lights:
                if light.startswith("Group:"):
                    name = light[6:]
                    index_set = self.group_indices
                    set_func = self.bridge.set_group
                else:
                    name = light
                    index_set = self.light_indices
                    set_func = self.bridge.set_light
                
                idx = index_set.get(name)
                if idx:
                    set_func(idx, preset.phue_dict())
                else:
                    print("Warning: Light or group with name '{}' unknown.".format(name))
