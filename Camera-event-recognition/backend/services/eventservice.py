from repositories.repositories import EventsRepository, DATABASE


class EventService:
    def __init__(self):
        self.repository = EventsRepository(DATABASE)

    def insert_event(self, type, confidence, area_name, camera_name):
        event_id = self.repository.insert_event(type, confidence, area_name, camera_name)
        return event_id

    def get_events(self, date_from):
        database_events = self.repository.read_events(date_from)
        return self.parse_events(database_events)

    def parse_events(self, events):
        jsons = []
        for event in events:
            dic = {
                "id": str(event.id),
                "timestamp": str(event.timestamp),
                "confidence": str(event.confidence),
                "type": event.type,
                "camera": event.camera_name,
                "area": event.area_name
            }
            jsons.append(dic)
        return jsons
