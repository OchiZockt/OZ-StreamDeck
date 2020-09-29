import time
import functools

from PIL import Image
from StreamDeck.ImageHelpers import PILHelper

from Deck.Array import Array
from Deck.Button import Button

from Messages.Common import *

class Device:
    def __init__(self, manager, deck):
        self._manager = manager
        self._deck = deck
        self._rows = self._deck.KEY_ROWS
        self._cols = self._deck.KEY_COLS
        self._btnw = self._deck.KEY_PIXEL_WIDTH
        self._btnh = self._deck.KEY_PIXEL_HEIGHT
        self._root = None
        self._last_key_time = 0
        
        self._deck.open()
        self._deck.reset()
        self._deck.set_brightness(50)
        self._deck.set_key_callback(functools.partial(self.key_change_callback))
        
        self._rebuild_layout = True
        
        print("Started deck " + self.serial_number())

    def request_layout_rebuild(self):
        self._rebuild_layout = True
    
    def fg_color(self):
        return "#FFFFFF"
    
    def bg_color(self):
        return "#000000"

    def stop(self):
        serial_number = self.serial_number()
        print(f"Stopping deck {serial_number}...")
        
        if self._root:
            self._root.stop()
        
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
        
        now = time.time()
        if now - self._last_key_time < 0.1:
            return
        
        with self._manager.lock():
            try:
                self._last_key_time = now
                button = self._button_buffer.get(key // self._cols, key % self._cols)
                if button is not None:
                    button.pressed()
                    button.set_highlight()
            except Exception as e:
                print("Unhandled exception in key_change_callback: " + str(e))
            
            self.render()

    def tick(self):
        if self._root is None:
            return
        
        try:
            self._root.tick()
        except Exception as e:
            print("Unhandled exception in tick: " + str(e))
        
        self.render()

    def update_button_buffer(self):
        self._button_buffer = Array(self._rows, self._cols)
        if self._root is not None:
            self._root.update_button_buffer(self._button_buffer)

        # Fill unset buttons with dummy buttons.
        for i in range(0, self._rows*self._cols):
            b = self._button_buffer.get_by_index(i)
            if b is None:
                dummy_button = Button()
                dummy_button.set_device(self)
                dummy_button.set_parent(self)
                self._button_buffer.set_by_index(i, dummy_button)
        
        self._layout_dirty = False

    def render(self):
        force = False
        if self._rebuild_layout:
            self.update_button_buffer()
            force = True
            self._rebuild_layout = False
        
        unhighlight_button = None
        
        for i in range(0, self._rows*self._cols):
            b = self._button_buffer.get_by_index(i)
            if b.dirty() or force:
                image = b.render(self._btnw, self._btnh, force)
                if image is not None:
                    deck_image = PILHelper.to_native_format(self._deck, image)
                    self._deck.set_key_image(i, deck_image)
                    if b.get_and_clear_highlight():
                        unhighlight_button = i
        
        if unhighlight_button is not None:
            time.sleep(0.1)
            b = self._button_buffer.get_by_index(unhighlight_button)
            image = b.render(self._btnw, self._btnh, True)
            if image is not None:
                deck_image = PILHelper.to_native_format(self._deck, image)
                self._deck.set_key_image(unhighlight_button, deck_image)

    def route(self, target, msg):
        if target == FRONTEND:
            if self._root:
                self._root.route(target, msg)
                self.render()
        
        elif target == BACKEND:
            self._manager.route(target, msg)
