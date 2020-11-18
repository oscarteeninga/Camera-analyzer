from config.cameraconfig import CameraConfig
from repositories.repositories import CamerasRepository, DATABASE
from services.cacheservice import cache, Dictionaries


class CameraService:
    def __init__(self):
        self.repository = CamerasRepository(DATABASE)

    def get_camera_name_id_mapping(self):
        id_to_name = {}
        name_to_id = {}
        for camera in self.repository.read_cameras():
            id_to_name[camera[0]] = camera[1]
            name_to_id[camera[1]] = camera[0]
        return id_to_name, name_to_id

    def add_config(self, config: CameraConfig):
        self.repository.insert_camera(config.id, config.ip, config.username, config.password)

    def update_config(self, id, ip, username, password):
        self.repository.update_camera(id, ip, username, password)

    def delete_config(self, id):
        self.repository.delete_camera(id)

    def get_config(self, id):
        return CameraConfig.from_list(self.repository.read_camera(id))

    def get_configs(self):
        return [CameraConfig.from_list(camera) for camera in self.repository.read_cameras()]

    def get_ips(self):
        return [config.ip for config in self.get_configs()]

    def get_config_json(self, id):
        conf = self.get_config(id)
        return conf.to_json() if conf else None

    def get_configs_json(self):
        return [camera.to_json() for camera in self.get_configs()]
