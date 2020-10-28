from model.repository import Repository

DATABASE = "events"


class EventService:
    def __init__(self):
        self.repository = Repository(DATABASE)

    def get_events(self):
        # database_events = self.repository.read()
        # todo fetch events from db and parse areas
        return [{
            "type": "car",
            "area": "A",
            "confidence": "0.44",
            "device": "192.168.1.110",
            "timestamp": "1603873871"
        }]
