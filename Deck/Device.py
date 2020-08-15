from time import time
from functools import partial
from threading import Lock

from StreamDeck.ImageHelpers import PILHelper

from Deck.Array import Array
from Deck.Button import Button

class Device:
    def __init__(self, deck):
        self._deck = deck
        self._rows = self._deck.KEY_ROWS
        self._cols = self._deck.KEY_COLS
        self._btnw = self._deck.KEY_PIXEL_WIDTH
        self._btnh = self._deck.KEY_PIXEL_HEIGHT
        self._root = None
        self._last_key_time = 0
        self._lock = Lock()
        
        self._deck.open()
        self._deck.reset()
        self._deck.set_brightness(50)
        self._deck.set_key_callback(partial(self.key_change_callback))
        
        self._rebuild_layout = True
        self._refresh_full = True
        self._refresh = True
        
        print("Started deck " + self.serial_number())

    def request_layout_rebuild(self):
        self._rebuild_layout = True
    
    def request_full_refresh(self):
        self._full_refresh = True
    
    def request_refresh(self):
        self._refresh = True

    def fg_color(self):
        return "#FFFFFF"
    
    def bg_color(self):
        return "#000000"

    def stop(self):
        serial_number = self.serial_number()
        print(f"Stopping deck {serial_number}...")
        with self._lock:
            self._deck.reset()
            self._deck.set_brightness(0)
            self._deck.close()
        print(f"Stopped deck {serial_number}.")
    
    def serial_number(self):
        return self._deck.get_serial_number()
    
    def print_info(self):
        print(self._deck)
        print(f"    Serial number: {self._deck.get_serial_number()}")

    def set_root_module(self, module):
        module.set_device(self)
        module.set_parent(self)
        self._root = module
        self.request_layout_rebuild()
        self.render()

    def key_change_callback(self, deck, key, state):
        if not state:
            return
        
        now = time()
        if now - self._last_key_time < 0.1:
            return
        
        with self._lock:
            try:
                self._last_key_time = now
                button = self._button_buffer.get(key // self._cols, key % self._cols)
                if button is not None:
                    button.pressed()
            except Exception as e:
                print("Unhandled exception in key_change_callback: " + str(e))
            
            self.check_refresh()

    def tick(self):
        if self._root is None:
            return
        
        with self._lock:
            try:
                self._root.tick()
            except Exception as e:
                print("Unhandled exception in tick: " + str(e))
            
            self.check_refresh()

    def check_refresh(self):
        if self._rebuild_layout:
            self.render(True)
            self._rebuild_layout = False
            self._refresh_full = False
            self._refresh = False
        elif self._refresh_full:
            self.render(True)
            self._refresh_full = False
            self._refresh = False
        elif self._refresh:
            self.render()
            self._refresh = False

    def update_button_buffer(self):
        self._button_buffer = Array(self._rows, self._cols)
        if self._root is not None:
            self._root.update_button_buffer(self._button_buffer)

        # Fill unset buttons with dummy buttons.
        for r in range(0, self._rows):
            for c in range(0, self._cols):
                b = self._button_buffer.get(r, c)
                if b is None:
                    dummy_button = Button()
                    dummy_button.set_device(self)
                    dummy_button.set_parent(self)
                    self._button_buffer.set(r, c, dummy_button)
        
        self._layout_dirty = False

    def render(self, force = False):
        if self._rebuild_layout:
            self.update_button_buffer()
            force = True
            self._rebuild_layout = False
        
        for r in range(0, self._rows):
            for c in range(0, self._cols):
                b = self._button_buffer.get(r, c)
                if b.dirty() or force:
                    image = b.render(self._btnw, self._btnh, force)
                    if image is not None:
                        deck_image = PILHelper.to_native_format(self._deck, image)
                        self._deck.set_key_image(r * self._cols + c, deck_image)
