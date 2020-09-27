import datetime
import os

from Utils.Timestamp import Timestamp

class TimestampManager:
    def __init__(self, directory):
        self._timestamps = {
            "Record": TS(os.path.join(directory, "record")),
            "StrRec": TS(),
            "Stream": TS(os.path.join(directory, "stream")),
            "Episode": TS()
        }
    
    def get(self, name):
        return self._timestamps.get(name)
    
    def mark_all(self, tag):
        for name, ts in self._timestamps.items():
            ts.mark(tag)

class TS:
    def __init__(self, filename = None):
        self._running = False
        self._timestamp = None
        self._filename = filename
        self._file = None
    
    def reset(self):
        if self._timestamp is not None:
            self._timestamp.reset()
    
    def running(self):
        return self._running
    
    def set_running(self, running):
        self._running = running
        if running:
            self._timestamp = Timestamp()
            
            if self._filename is not None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{self._filename}_{timestamp}.txt"
                try:
                    self._file = open(filename, "w")
                except:
                    print("WARNING: Could not open output file.")
                    return
        else:
            self._timestamp = None
            
            if self._file is not None:
                self._file.close()
                self._file = None
    
    def toggle_running(self):
        self.set_running(not self._running)
    
    def for_display(self):
        if self._running:
            return self._timestamp.for_display()
        else:
            return "–"
    
    def mark(self, tag):
        if self._file is not None:
            line = self._timestamp.for_file() + ": " + tag
            print(line)
            self._file.write(line + "\n")
            self._file.flush()
