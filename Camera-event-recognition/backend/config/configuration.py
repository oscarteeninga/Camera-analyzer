from config.cameraconfig import CameraConfig
from config.yoloconfig import YoloConfig


class Configuration:
    def __init__(self, camera_config, yolo_config):
        self.camera_config = camera_config
        self.yolo_config = yolo_config

    @classmethod
    def from_arguments(cls,
                       camera_ip,
                       camera_user,
                       camera_password,
                       camera_fps=25,
                       batch_size=608,
                       weights_file="bin/yolov3.weights",
                       classes_file="yolov3.txt",
                       config_file="cfg/yolov3.cfg"):
        camera_config = CameraConfig(camera_ip, camera_user, camera_password, camera_fps)
        yolo_config = YoloConfig(batch_size, weights_file, classes_file, config_file)
        return Configuration(camera_config, yolo_config)

    def __str__(self):
        return "config"
