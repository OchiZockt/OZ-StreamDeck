class FaceLightsMessage:
    pass

class _Settings:
    def __init__(self, on, brightness, color):
        self.on = on
        self.brightness = brightness
        self.color = color

class SetFaceLightCommand(FaceLightsMessage):
    def __init__(self, left_on, left_brightness, left_color, right_on, right_brightness, right_color):
        self.left = _Settings(left_on, left_brightness, left_color)
        self.right = _Settings(right_on, right_brightness, right_color)
