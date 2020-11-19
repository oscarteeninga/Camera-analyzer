import time

from repositories.repositories import EventsRepository, DATABASE


class EventService:
    def __init__(self):
        self.repository = EventsRepository(DATABASE)

    def insert_event(self, type, confidence, area_name, camera_name):
        timestamp = int(time.time() * 1000)

        event_id = self.repository.insert_event(type, timestamp, confidence, area_name, camera_name)
        return event_id

    def get_events(self, page, size, date_from):
        database_events = self.repository.read_events(page, size, date_from)
        return self.parse_events(database_events)

    def parse_events(self, events):
        jsons = []
        for event in events:
            dic = {
                "id": event[0],
                "timestamp": event[1],
                "confidence": event[2],
                "type": event[3],
                "camera": event[4],
                "area": event[5]
            }
            jsons.append(dic)
        return jsons
