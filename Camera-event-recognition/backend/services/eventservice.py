from repositories.repositories import EventsRepository, DATABASE
from services.areaservice import AreaService
from services.cameraservice import CameraService

area_service = AreaService()
camera_service = CameraService()


class EventService:
    def __init__(self):
        self.repository = EventsRepository(DATABASE)

    def get_events(self, page, size, date_from):
        database_events = self.repository.read_events(page, size, date_from)
        return self.parse_events(database_events)

    def parse_events(self, events):
        jsons = []
        for event in events:
            dic = {
                "id": event[0],
                "type": event[3],
                "confidence": event[2],
                "camera": camera_service.get_camera_name(event[8]) if event[
                                                                          8] is not None else None,
                "timestamp": event[1],
                "area": area_service.recognize_area(event[4], event[5], event[6], event[7])
            }
            jsons.append(dic)
        return jsons
