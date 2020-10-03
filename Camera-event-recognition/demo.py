from receiver import CameraAnalyzer, DetectBox, YoloConfig, CameraConfig
from repository import Repository
from sys import argv

repository = Repository("demo.db")
camera_config = CameraConfig("192.168.0.119", "admin", "camera123", 25)
yolo_config = YoloConfig("bin/yolov3.weights", "yolov3.txt", "cfg/yolov3.cfg", int(argv[1]))
detect_box = DetectBox(300, 300, 600, 600)

camera_analyzer = CameraAnalyzer(camera_config, yolo_config, repository)
camera_analyzer.set_detect_box(detect_box)
camera_analyzer.video(True, True)
