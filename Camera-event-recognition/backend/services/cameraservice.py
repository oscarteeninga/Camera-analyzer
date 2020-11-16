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
        id = self.repository.insert_camera(config.name, config.ip, config.username, config.password)
        ip_to_name, name_to_ip = self.get_camera_name_id_mapping()
        cache.set(Dictionaries.CAMERA_IP_TO_NAME, ip_to_name)
        cache.set(Dictionaries.CAMERA_NAME_TO_IP, name_to_ip)
        return id

    def update_config(self, id, name, ip, username, password):
        self.repository.update_camera(id, name, ip, username, password)
        ip_to_name, name_to_ip = self.get_camera_name_id_mapping()
        cache.set(Dictionaries.CAMERA_IP_TO_NAME, ip_to_name)
        cache.set(Dictionaries.CAMERA_NAME_TO_IP, name_to_ip)
        return id

    def delete_config(self, id):
        self.repository.delete_camera(id)
        ip_to_name, name_to_ip = self.get_camera_name_id_mapping()
        cache.set(Dictionaries.CAMERA_IP_TO_NAME, ip_to_name)
        cache.set(Dictionaries.CAMERA_NAME_TO_IP, name_to_ip)

    def get_config(self, name):
        return CameraConfig.from_list(self.repository.read_camera(name))

    def get_configs(self):
        return [CameraConfig.from_list(camera) for camera in self.repository.read_cameras()]

    def get_ips(self):
        return [config.ip for config in self.get_configs()]

    def get_camera(self, id):
        camera = self.repository.read_camera(id)
        return {
            "id": camera[0],
            "name": camera[1],
            "ip": camera[2],
            "user": camera[3],
            "password": camera[4]
        }

    def get_cameras(self):
        jsons = []
        for camera in self.repository.read_cameras():
            dic = {
                "id": camera[0],
                "name": camera[1],
                "ip": camera[2],
                "user": camera[3],
                "password": camera[4]
            }
            jsons.append(dic)
        return jsons
