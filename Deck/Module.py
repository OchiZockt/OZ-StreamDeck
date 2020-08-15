from Deck.Item import Item

class Module(Item):
    def __init__(self, fg_color = None, bg_color = None):
        super().__init__(fg_color, bg_color)
        self._buttons = {}
        self._modules = []
        self._enabled = True
    
    def set_device(self, device):
        super().set_device(device)
        for m in self._modules:
            m.module.set_device(device)
        for _, b in self._buttons.items():
            b.set_device(device)
    
    def set_enabled(self, enabled):
        self._enabled = enabled
    
    def button(self, row, col):
        return self._buttons.get((row, col))
    
    def set_button(self, row, col, button):
        button.set_device(self._device)
        button.set_parent(self)
        self._buttons[(row, col)] = button

    def add_module(self, row, col, module):
        module.set_device(self._device)
        module.set_parent(self)
        self._modules.append(SubModule(module, row, col))

    def update_button_buffer(self, button_buffer):
        if not self._enabled:
            return
        
        # Update submodules recursively first.
        for m in self._modules:
            m.module.update_button_buffer(button_buffer.view(m.drow, m.dcol))
        
        # Now insert our buttons.
        for pos, btn in self._buttons.items():
            row, col = pos
            if button_buffer.get(row, col) is None:
                button_buffer.set(row, col, btn)

    def tick(self):
        for m in self._modules:
            m.module.tick()
        for _, b in self._buttons.items():
            b.tick()

class SubModule:
    def __init__(self, module, drow, dcol):
        self.module = module
        self.drow = drow
        self.dcol = dcol
