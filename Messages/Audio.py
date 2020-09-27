class AudioMessage:
    pass

class VolumeMessage(AudioMessage):
    def __init__(self, track, volume):
        self.track = track
        self.volume = volume

class MuteMessage(AudioMessage):
    def __init__(self, track, muted):
        self.track = track
        self.muted = muted
