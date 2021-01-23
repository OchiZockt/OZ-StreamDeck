import time

from Deck.Manager import Manager
from Modules.StreamDeck import StreamDeck
from Modules.StreamDeckXL import StreamDeckXL

manager = Manager()

#streamdeck = manager.device("AL47I2C01794")
#if streamdeck is not None:
#    streamdeck.set_root_module(StreamDeck())

streamdeckxl = manager.device("CL44I1A01786")
if streamdeckxl is not None:
    streamdeckxl.set_root_module(StreamDeckXL())
else:
    print("Error: StreamDeckXL not found.")

try:
    manager.run()
except KeyboardInterrupt:
    print()
    manager.stop()
except Exception as e:
    print("Unhandled exception in manager: " + str(e))
    print("Attempting to stop manager...")
    manager.stop()
    print("Done.")
    raise e
