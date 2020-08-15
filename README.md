# OZ-StreamDeck
Stream Deck controller for OBS, Hue, Elgato Key Light, OSC, MPRIS, etc. while streaming or recording

## Dependencies

I'm using the following supporting libraries:

* Elgato Stream Deck: https://github.com/abcminiuser/python-elgato-streamdeck
* Elgato Key Light: https://pypi.org/project/leglight/
* Philips Hue: https://pypi.org/project/phue/
* OBS WebSockets: https://github.com/Palakis/obs-websocket
* python-osc (Open Sound Control, for controlling REAPER): https://pypi.org/project/python-osc/

## Overview

* "Deck" contains general-purpose classes encapsulating Stream Deck devices, buttons, groups of buttons, etc.
* "Connectors" contains vendor-specific helper classes for controlling devices or external software
* "Modules" contains user-/project-specific definitions of what should be shown on the Stream Decks and how to handle input
* "Utils" contains small utility or helper classes
