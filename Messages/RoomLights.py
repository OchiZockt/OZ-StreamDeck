class RoomLightsMessage:
    pass

class SetPresetCommand(RoomLightsMessage):
    def __init__(self, preset):
        self.preset = preset
