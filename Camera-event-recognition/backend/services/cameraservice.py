from config.cameraconfig import CameraConfig
from repositories.repositories import CamerasRepository, DATABASE


class CameraService:
    def __init__(self):
        self.repository = CamerasRepository(DATABASE)

    def get_camera_name(self, id):
        return self.repository.read_camera(id).name

    def add_config(self, config: CameraConfig):
        self.repository.insert_camera(config.name, config.ip, config.username, config.password, config.fps)

    def get_config(self, id):
        return CameraConfig.from_list(self.repository.read_camera(id))

    def get_configs(self):
        for c in self.repository.read_cameras():
            yield CameraConfig.from_list(c)

    def get_ips(self):
        for config in self.get_configs():
            yield config.ip
