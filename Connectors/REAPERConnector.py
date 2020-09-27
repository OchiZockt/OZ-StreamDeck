import requests

class REAPERConnector:
    def __init__(self, backend, host, port):
        self._backend = backend
        self._host = host
        self._port = port
    
    def send(self, msg):
        self._backend.recv_from_backend(msg)
    
    def recv(self, msg):
        pass
    
    def get_volume(self, track):
        try:
            request = requests.get(f"http://{self._host}:{self._port}/_/TRACK/{track}")
            response = request.text
            print(response)
            return 0
        except:
            print(f"Error fetching volume for REAPER track {track}.")
