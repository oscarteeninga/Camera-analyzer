from sys import argv

from backend.config.configuration import Configuration

from backend.config.cameraconfig import CameraConfig
from backend.config.yoloconfig import YoloConfig
from backend.model.receiver import CameraAnalyzer, DetectBox
from backend.repositories.repositories import Repository

repository = Repository("demo.db")
camera_config = CameraConfig("192.168.0.119", "admin", "camera123", 25)
yolo_config = YoloConfig(int(argv[1]), "yolo/cfg/yolov3.weights", "yolo/cfg/yolov3.txt",
                         "yolo/cfg/yolov3.cfg")
detect_box = DetectBox(300, 200, 1000, 600)
configuration = Configuration(camera_config, yolo_config)

camera_analyzer = CameraAnalyzer(configuration, repository)
camera_analyzer.set_detect_box(detect_box)
camera_analyzer.video(True, False)
