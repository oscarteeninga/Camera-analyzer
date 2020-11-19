from sys import argv

from config.yoloconfig import YoloConfig
from model.analyzer import Analyzer
from services.areaservice import AreaService
from services.cameraservice import CameraService
from services.eventservice import EventService

event_service = EventService()
area_service = AreaService(event_service)
camera_service = CameraService(area_service)
camera_id = camera_service.add_config("kamera", "192.168.1.108", "admin", "camera123")
area_id = area_service.add_area(0.5, 0, 0, 1000, 1000, camera_id)
try:
    camera_config = camera_service.get_config(camera_id)
    yolo_config = YoloConfig(int(argv[1]), "../yolo/cfg/yolov3.weights", "../yolo/cfg/yolov3.txt",
                             "../yolo/cfg/yolov3.cfg")

    camera_analyzer = Analyzer(event_service, area_service, camera_config, yolo_config=yolo_config)
    camera_analyzer.video(False)
finally:
    camera_service.delete_config(camera_id)
    area_service.delete_area(area_id)
