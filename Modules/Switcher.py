from Deck.Button import Button
from Deck.Module import Module

COLOR_ACTIVE = "#7A00F4"
COLOR_INACTIVE = "#220055"

class Switcher(Module):
    def __init__(self, modules):
        super().__init__()
        
        self._current_module = None
        self._switch_modules = modules
        self._switch_buttons = {}
        
        idx = 0
        for name, module in modules.items():
            switch_button = SwitchButton(name)
            self.set_button(idx, 0, switch_button)
            self._switch_buttons[name] = switch_button
            idx = idx + 1
    
    def switch(self, module_name):
        for name, module in self._switch_modules.items():
            enabled = (name == module_name and name != self._current_module)
            module.set_enabled(enabled)
            self._switch_buttons[name].set_bg_color(COLOR_ACTIVE if enabled else COLOR_INACTIVE)
        
        if module_name == self._current_module:
            self._current_module = None
        else:
            self._current_module = module_name
        
        self.request_layout_rebuild()

class SwitchButton(Button):
    def __init__(self, display_name):
        super().__init__(text = display_name, bg_color = COLOR_INACTIVE)
    
    def pressed(self):
        self._parent.switch(self.text())
