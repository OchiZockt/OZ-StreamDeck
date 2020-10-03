from Deck.Module import Module

from Modules.Primary import Primary

class StreamDeckXL(Module):
    def __init__(self):
        super().__init__()
        
        self.add_module(0, 0, Primary())
