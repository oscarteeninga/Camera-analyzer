from config.cameraconfig import CameraConfig
from config.yoloconfig import YoloConfig


class Configuration:
    def __init__(self, camera_ip, camera_user, camera_password, batch_size):
        self.camera_config = CameraConfig(camera_ip, camera_user, camera_password)
        self.yolo_config = YoloConfig(batch_size)

    def __str__(self):
        return "config"
