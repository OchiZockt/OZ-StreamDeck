from Deck.Module import Module

from Modules.Checklist import Checklist
from Modules.Primary import Primary

class StreamDeckXL(Module):
    def __init__(self):
        super().__init__()
        
        self.add_module(0, 0, Primary())
        self.add_module(0, 0, Checklist())
