from leglight import LegLight

class LegConnector:
    def __init__(self, ip):
        try:
            self.leglight = LegLight(ip, 9123)
            print(self.leglight)
        except:
            print(f"LegLight connection to {ip} failed.")
    
    def set(self, on, brightness = 100, color = 3500):
        if on:
            self.leglight.on()
            self.leglight.brightness(brightness)
            self.leglight.color(color)
        else:
            self.leglight.off()
