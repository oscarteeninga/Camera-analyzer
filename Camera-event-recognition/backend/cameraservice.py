from model.repository import Repository

DATABASE = "cameras"


class CameraService:
    def __init__(self):
        self.repository = Repository(DATABASE)

    def get_camera_name(self, id):
        return self.repository.read_camera_name(id)
