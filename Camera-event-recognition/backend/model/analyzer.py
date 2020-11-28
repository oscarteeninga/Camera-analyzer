import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
from config.areaconfig import AreaConfig
from config.cameraconfig import CameraConfig
from config.yoloconfig import YoloConfig
from model.receiver import Receiver
from services.eventservice import EventService

CONSOLE_INFO = 1


class Analyzer:

    def __init__(self, event_service, area_service, camera_config: CameraConfig,
                 yolo_config=YoloConfig.basic()):
        self.on = True
        self.camera_config = camera_config
        self.yolo_config = yolo_config
        self.event_service: EventService = event_service
        self.area_service = area_service
        self.capture = Receiver(camera_config)
        self.net = self.yolo_config.net()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def stop(self):
        self.on = False
        self.capture.stop()

    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    def draw_bounding_box(self, image, class_id, x, y, w, h):
        label = str(self.yolo_config.classes[class_id])
        color = self.yolo_config.colors[class_id]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    @staticmethod
    def draw_area_box(image, area: AreaConfig):
        label = "area " + area.name
        color = area.color
        x1, y1, x2, y2 = area.x, area.y, area.x + area.w, area.y + area.h
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1 - 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def process_frame(self, image):
        if self.camera_config.fit_video_to_areas:
            x, y, width, height = self.area_service.get_camera_image_coords_trimmed_to_areas(
                self.camera_config.id)
            image = self.trim_to_areas(image, x, y, width, height)
        width = image.shape[1]
        height = image.shape[0]

        blob = cv2.dnn.blobFromImage(
            image, self.yolo_config.scale,
            (self.yolo_config.batch_size, self.yolo_config.batch_size),
            (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            self.executor.submit(self.process_detection, out, width, height, class_ids, confidences,
                                 boxes)

    def process_detection(self, out, width, height, class_ids, confidences, boxes):
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2

                label = str(self.yolo_config.classes[class_id])
                self.area_service.insert_events_for_areas(self.camera_config, label,
                                                          confidence, x, y, w, h)
                print("Detected " + label + " with " + str(confidence) + " confidence")

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    def trim_to_areas(self, image, x, y, width, height):
        return image[y:y + height, x:x + width]

    def one_process_episode(self):
        frame = self.capture.read()
        begin_time = time.time()
        self.process_frame(frame)

        if CONSOLE_INFO == 1:
            print("Process time: " + str(time.time() - begin_time))
        cv2.waitKey(1)

    def video(self):

        if CONSOLE_INFO == 1:
            print("Begin video processing...")

        while self.on:
            self.one_process_episode()

        print("Ended video processing...")
