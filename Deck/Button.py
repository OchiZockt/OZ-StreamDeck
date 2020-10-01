from PIL import Image, ImageDraw, ImageFont

from Deck.Item import Item
from Messages.Common import *

class Button(Item):
    def __init__(self, text = "", fg_color = None, bg_color = None, font_size = 18):
        super().__init__(fg_color, bg_color)
        self._text = text
        self._font_size = font_size
        self._dirty = True

    def dirty(self):
        return self._dirty
    
    def set_dirty(self):
        self._dirty = True

    def text(self):
        return self._text

    def render(self, width, height, force):
        if not self.dirty() and not force:
            return None
        
        image = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(image)
        
        draw.rectangle([(0, 0), (width-1, height-1)], fill = self.bg_color())
        
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", self._font_size)
        
        text = self.text()
        label_w, label_h = draw.textsize(text, font = font)
        label_pos = ((width - label_w) // 2, (height // 2) - (label_h // 2))
        draw.text(label_pos, text = text, fill = self.fg_color(), font = font)
        
        self._dirty = False
        
        return image

    def pressed(self):
        pass
    
    def tick(self):
        pass

    def stop(self):
        pass
    
    def recv(self, msg):
        pass
    
    def send_to_frontend(self, msg):
        self._device.route(FRONTEND, msg)

    def send_to_backend(self, msg):
        self._device.route(BACKEND, msg)
