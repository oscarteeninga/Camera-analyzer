from config.cameraconfig import CameraConfig
from repositories.repositories import CamerasRepository, DATABASE


class CameraService:
    def __init__(self):
        self.repository = CamerasRepository(DATABASE)

    def get_camera_name(self, id):
        return self.repository.read_camera(id)[1]

    def add_config(self, config: CameraConfig):
        self.repository.insert_camera(config.name, config.ip, config.username, config.password)

    def get_config(self, name):
        return CameraConfig.from_list(self.repository.read_camera(name))

    def get_configs(self):
        return [CameraConfig.from_list(camera) for camera in self.repository.read_cameras()]

    def get_ips(self):
        return [config.ip for config in self.get_configs()]

    def get_names(self):
        return [config.name for config in self.get_configs()]
