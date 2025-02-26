class Camera:
    def __init__(self):
        import libcamera
        self.camera_manager = libcamera.CameraManager()
        self.camera = None
        self.stream = None

    def start(self):
        self.camera_manager.start()
        self.camera = self.camera_manager.get_camera("camera0")
        self.camera.configure()
        self.stream = self.camera.start_stream()

    def stop(self):
        if self.stream:
            self.stream.stop()
        if self.camera:
            self.camera.release()
        self.camera_manager.stop()

    def get_frame(self):
        if self.stream:
            frame = self.stream.get_frame()
            return frame
        return None