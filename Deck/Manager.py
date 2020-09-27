import signal
from threading import Lock, Thread
from time import sleep
from queue import Queue

from StreamDeck import DeviceManager

from Deck.Device import Device
from Deck.Backend import Backend
from Messages.Common import *

class Manager:
    def __init__(self):
        print("Starting manager...")
        
        self._devices = []
        for d in DeviceManager.DeviceManager().enumerate():
            device = Device(self, d)
            self._devices.append(device)
        
        self._stop = False
        self._lock = Lock()
        self._msg_queue = Queue()
        self._backend = Backend(self)
        
        print("Started manager.")

    def handle_sigint(self, signal, frame):
        print()
        print("Stopping...")
        with self._lock:
            self._stop = True

    def lock(self):
        return self._lock

    def stop(self):
        print("Stopping manager...")
        self._stop = True
        for d in self._devices:
            d.stop()
        self._backend.stop()
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
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        Thread(target = self.msg_queue_thread).start()
        
        for d in self._devices:
            d.render()
        while True:
            with self._lock:
                if self._stop:
                    self.stop()
                    break
                for d in self._devices:
                    d.tick()
            sleep(1.0)

    def msg_queue_thread(self):
        MSG_QUEUE_DEBUG = False
        def msg_queue_debug(msg):
            if MSG_QUEUE_DEBUG:
                print(msg)
        
        while True:
            if self._stop:
                break
            try:
                target, msg = self._msg_queue.get(timeout = 0.5)
                msg_queue_debug("Getting lock for message processing...")
                with self._lock:
                    try:
                        msg_queue_debug("Processing message " + str(msg))
                        if target == FRONTEND:
                            for d in self._devices:
                                d.route(target, msg)
                        elif target == BACKEND:
                            self._backend.route(target, msg)
                    except Exception as e:
                        print("Exception while processing message:\n\n" + str(e) + "\n")
            except:
                pass
        print("Message queue stopped.")

    def route(self, target, msg):
        self._msg_queue.put((target, msg))
