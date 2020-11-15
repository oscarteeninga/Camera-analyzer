from model.analyzer import CameraAnalyzer
from config.cameraconfig import CameraConfig
from config.yoloconfig import YoloConfig
from sys import argv

camera_config = CameraConfig("kamera", "192.168.0.119", "admin", "camera123")
yolo_config = YoloConfig(int(argv[1]), "yolo/cfg/yolov3.weights", "yolo/cfg/yolov3.txt",
                         "yolo/cfg/yolov3.cfg")

camera_analyzer = CameraAnalyzer(camera_config, yolo_config=yolo_config)
camera_analyzer.video(True)
