class Item:
    def __init__(self, fg_color, bg_color):
        self._device = None
        self._parent = None
        self._fg_color = fg_color
        self._bg_color = bg_color
    
    def set_device(self, device):
        self._device = device
    
    def set_parent(self, parent):
        self._parent = parent

    def request_refresh(self):
        if self._device is None:
            raise Exception("Refresh requested with unset device.")
        self._device.request_refresh()
    
    def request_full_refresh(self):
        if self._device is None:
            raise Exception("Full refresh requested with unset device.")
        self._device.request_full_refresh()
    
    def request_layout_rebuild(self):
        if self._device is None:
            raise Exception("Layout rebuild requested with unset device.")
        self._device.request_layout_rebuild()
    
    def fg_color(self):
        if self._fg_color is not None:
            return self._fg_color
        else:
            return self._parent.fg_color()

    def bg_color(self):
        if self._bg_color is not None:
            return self._bg_color
        else:
            return self._parent.bg_color()
    
    def set_fg_color(self, fg_color):
        self._fg_color = fg_color
    
    def set_bg_color(self, bg_color):
        self._bg_color = bg_color
