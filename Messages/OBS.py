class OBSMessage:
    pass

class SwitchSceneCommand(OBSMessage):
    def __init__(self, scene_name):
        self.scene_name = scene_name

class StartStopCommand(OBSMessage):
    def __init__(self, obs_kind, ctl_kind, running):
        self.obs_kind = obs_kind
        self.ctl_kind = ctl_kind
        self.running = running
