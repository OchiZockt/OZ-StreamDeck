from Deck.Connector import Connector

import requests

class REAPERConnector(Connector):
    def __init__(self, backend, host, port):
        super().__init__(backend)
        
        self._host = host
        self._port = port
    
    def get_volume(self, track):
        try:
            request = requests.get(f"http://{self._host}:{self._port}/_/TRACK/{track}")
            response = request.text
            print(response)
            return 0
        except:
            print(f"Error fetching volume for REAPER track {track}.")
