from config.cameraconfig import CameraConfig
from repositories.repositories import CamerasRepository, DATABASE

import cv2


class CameraService:
    def __init__(self, area_service):
        self.repository = CamerasRepository(DATABASE)
        self.area_service = area_service

    def add_config(self, name, ip, username, password,fit_video_to_areas):
        camera_id = self.repository.insert_camera(name, ip, username, password,fit_video_to_areas)
        # self.area_service.insert_area(0, 0, 0, 0, 0, camera_id)
        return camera_id

    def update_config(self, id, name, ip, username, password,fit_video_to_areas):
        self.repository.update_camera(id, name, ip, username, password,fit_video_to_areas)

    def delete_config(self, id):
        self.repository.delete_camera(id)

    def get_config(self, id):
        conf = self.repository.read_camera(id)
        return CameraConfig.from_list(conf) if conf else None

    def get_configs(self):
        configs = [CameraConfig.from_list(camera) for camera in self.repository.read_cameras()]
        return configs

    def get_ips(self):
        return [config.ip for config in self.get_configs()]

    def get_config_json(self, id):
        conf = self.get_config(id)
        config_json = conf.to_json() if conf else None
        return config_json

    def get_configs_json(self):
        return [camera.to_json() for camera in self.get_configs()]

    def get_image(self, id):
        conf = self.get_config(id)
        if conf:
            cap = conf.capture()
            if cap.grab():
                ret, image = cap.read()
                (flag, encodedImage) = cv2.imencode(".jpg", image)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
            else:
                yield "Cannot connect to device for config " + str(conf)
        else:
            yield "Device config does not exist"

    def get_video(self, id):
        conf = self.get_config(id)
        if conf:
            cap = conf.capture()
            while cap.grab():
                ret, image = cap.read()
                (flag, encodedImage) = cv2.imencode(".jpg", image)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
            else:
                yield "Cannot connect to device for config " + str(conf)
        else:
            yield "Device config does not exist"

