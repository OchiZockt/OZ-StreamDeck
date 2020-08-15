import time

class Timestamp:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.start_time = time.time()
    
    def delta(self):
        return time.time() - self.start_time
    
    def f(self):
        return int(self.delta() * 100) % 100
    
    def s(self):
        return int(self.delta()) % 60
    
    def m(self):
        return int(self.delta()) // 60 % 60
    
    def h(self):
        return int(self.delta()) // 3600
    
    def for_display(self):
        return f"{self.h()}:{self.m():02}:{self.s():02}"
    
    def for_file(self):
        return f"{self.h():02}:{self.m():02}:{self.s():02}:{self.f():02}"
