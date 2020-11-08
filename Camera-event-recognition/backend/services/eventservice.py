import json

from services.areaservice import AreaService
from services.cameraservice import CameraService
from repositories.repositories import EventsRepository, DATABASE

area_service = AreaService()
camera_service = CameraService()


class EventService:
    def __init__(self):
        self.repository = EventsRepository(DATABASE)

    def get_events(self, date_from):
        database_events = self.repository.read_events(date_from)
        return self.parse_events(database_events)

    def parse_events(self, events):
        jsons = []
        for event in events:
            dic = {
                "type": event[2],
                "confidence": event[1],
                "camera": camera_service.get_camera_name(event[7]),
                "timestamp": event[0],
                "area": area_service.recognize_area(event[3], event[4], event[5], event[6])
            }
            jsons.append(dic)
        return json.dumps(jsons)
