from threading import Lock
from time import sleep

from StreamDeck import DeviceManager

from Deck.Device import Device

class Manager:
    def __init__(self):
        print("Starting manager...")
        self._devices = []
        for d in DeviceManager.DeviceManager().enumerate():
            device = Device(d)
            self._devices.append(device)
        
        self._stop = False
        self._lock = Lock()
        print("Started manager.")

    def stop(self):
        print("Stopping manager...")
        with self._lock:
            self._stop = True
            for d in self._devices:
                d.stop()
        print("Manager stopped.")

    def list(self):
        for d in self._devices:
            d.print_info()

    def device(self, serial = None):
        if serial is None:
            return self._devices[0]
        
        for d in self._devices:
            if d.serial_number() == serial:
                return d
        
        return None

    def run(self):
        for d in self._devices:
            d.render()
        while not self._stop:
            with self._lock:
                for d in self._devices:
                    d.tick()
            sleep(1.0)
