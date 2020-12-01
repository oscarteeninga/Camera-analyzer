from sys import argv

from config.yoloconfig import YoloConfig
from model.analyzer import Analyzer
from services.areaservice import AreaService
from services.cameraservice import CameraService
from services.eventservice import EventService

event_service = EventService()
area_service = AreaService(event_service)
camera_service = CameraService(area_service)
yolo_config = YoloConfig(608, "yolo/cfg/yolov3-320.weights", "yolo/cfg/yolov3.txt", "yolo/cfg/yolov3-320.cfg")
camera_id = camera_service.add_config("kamera", "192.168.0.119", "admin", "camera123", False)
area_id = area_service.insert_area(0.5, 50, 50, 600, 600, camera_id)
try:
    camera_config = camera_service.get_config(camera_id)
    camera_analyzer = Analyzer(event_service, area_service, camera_config, yolo_config)
    # camera_analyzer.set_show_size(700, 500)
    camera_analyzer.video()

finally:
    camera_service.delete_config(camera_id)
    for area in area_service.get_areas():
        area_service.delete_area(area.id)
