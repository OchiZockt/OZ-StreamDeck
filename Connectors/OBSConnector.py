import obswebsocket, obswebsocket.requests, obswebsocket.events, obswebsocket.exceptions

class OBSConnector:
    def __init__(self, ip, port):
        self.obs = None
        self.ip = ip
        self.port = port
        self.ensure_connection()
    
    @staticmethod
    def on_event(message):
        pass
    
    @staticmethod
    def on_switch(message):
        pass
    
    def ensure_connection(self):
        if self.obs is not None:
            return True
        
        self.obs = obswebsocket.obsws(self.ip, self.port)
        try:
            self.obs.connect()
            print("OBS connected")
            return True
        except obswebsocket.exceptions.ConnectionFailure:
            print("OBS connection failure")
            self.obs = None
            return False
    
    def call(self, request):
        if not self.ensure_connection():
            return
        
        try:
            result = self.obs.call(request)
            return result.datain
        except:
            print("OBS websocket exception")
            self.obs = None
            return None
    
    def switch_scene(self, scene_name):
        self.call(obswebsocket.requests.SetCurrentScene(scene_name))
    
    def get_status(self):
        return self.call(obswebsocket.requests.GetStreamingStatus())
    
    def set_recording(self, state):
        if state:
            self.start_recording()
        else:
            self.stop_recording()
    
    def set_streaming(self, state):
        if state:
            self.start_streaming()
        else:
            self.stop_streaming()
    
    def start_recording(self):
        self.call(obswebsocket.requests.StartRecording())
    
    def stop_recording(self):
        self.call(obswebsocket.requests.StopRecording())
    
    def start_streaming(self):
        self.call(obswebsocket.requests.StartStreaming())
    
    def stop_streaming(self):
        self.call(obswebsocket.requests.StopStreaming())
