from model.repository import Repository

DATABASE = "events"


class EventService:
    def __init__(self):
        self.repository = Repository(DATABASE)

    def get_events(self):
        database_events = self.repository.read()
        return database_events
