class AudioMessage:
    pass

class SetMuteCommand(AudioMessage):
    def __init__(self, track, muted):
        self.track = track
        self.muted = muted
