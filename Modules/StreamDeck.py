from Deck.Module import Module
from Deck.Button import Button

class StreamDeck(Module):
    def __init__(self):
        super().__init__()
        button = Button("StreamDeck")
        self.set_button(0, 0, button)
