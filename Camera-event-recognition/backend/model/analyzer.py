import os
import sys

sys.path.append(os.path.join("backend"))
import time
import cv2
import threading
import numpy as np
from config.areaconfig import AreaConfig
from config.cameraconfig import CameraConfig
from config.yoloconfig import YoloConfig
from model.receiver import Receiver
from model.sender import Sender
from services.eventservice import EventService
from services.areaservice import AreaService

CONSOLE_INFO = 0
SHOW = 1


class Analyzer:

    def __init__(self, event_service, area_service, camera_config: CameraConfig, yolo_config=YoloConfig.basic()):
        self.camera_config = camera_config
        self.yolo_config = yolo_config

        self.event_service: EventService = event_service
        self.area_service: AreaService = area_service

        self.capture = Receiver(camera_config)
        self.sender = Sender()

        self.net = self.yolo_config.net()

        self.show_size = None
        self.on = True

    def stop(self):
        self.on = False
        self.capture.stop()

    def set_show_size(self, width, height):
        self.show_size = (width, height)

    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    def draw_bounding_box(self, image, class_id, confidence, box):
        x1, y1, x2, y2 = box[0], box[1], box[0] + box[2], box[1] + box[3]
        label = str(self.yolo_config.classes[class_id])
        color = self.yolo_config.colors[class_id]
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label + " " + str(confidence), (x1 - 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    @staticmethod
    def draw_area_box(image, area: AreaConfig):
        color = area.color
        w = area.width if area.width else image.shape[1]
        h = area.height if area.height else image.shape[0]
        x1, y1, x2, y2 = area.x, area.y, area.x + w, area.y + h
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, "area " + area.name + " " + str(area.coverage_required),
                    (x1 + 12, y1 + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def put_image(self, image, indices, class_ids, boxes, confidences):
        for i in indices:
            i = i[0]
            self.draw_bounding_box(image, class_ids[i], confidences[i], boxes[i])
        if self.camera_config.fit_video_to_areas:
            for area in self.area_service.change_absolute_coords_to_relative(self.camera_config.id):
                self.draw_area_box(image, area)
        else:
            for area in self.area_service.areas_cached:
                if area.camera_id == self.camera_config.id:
                    self.draw_area_box(image, area)

        if self.show_size:
            image = cv2.resize(image, self.show_size)

        self.sender.put(image)

    def process_frame(self, image):
        if self.camera_config.fit_video_to_areas:
            coords = self.area_service.get_camera_areas_coords(self.camera_config.id)
            if coords:
                x, y, width, height = coords
                if width + height != 0:
                    image = image[y:y + height, x:x + width]

        blob = cv2.dnn.blobFromImage(
            image, self.yolo_config.scale,
            (self.yolo_config.batch_size, self.yolo_config.batch_size),
            (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())

        width = image.shape[1]
        height = image.shape[0]

        threading.Thread(target=self.process_detection, args=(outs, width, height, image,)).start()

    def process_detection(self, outs, width, height, image):
        class_ids = []
        boxes = []
        confidences = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.yolo_config.conf_threshold, self.yolo_config.nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            label = str(self.yolo_config.classes[class_ids[i]])

            if CONSOLE_INFO:
                print("Detected " + label + " with " + str(confidences[i]) + " confidence")

            self.area_service.insert_event(self.camera_config, label, confidences[i], box[0], box[1], box[2], box[3])

        if SHOW:
            self.put_image(image, indices, class_ids, boxes, confidences)

    def one_process_episode(self):
        frame = self.capture.read()
        begin_time = time.time()
        self.process_frame(frame)

        if CONSOLE_INFO:
            print("Process time: " + str(time.time() - begin_time))

    def video(self):

        if CONSOLE_INFO:
            print("Begin video processing...")

        while self.on:
            self.one_process_episode()

        if CONSOLE_INFO:
            print("Ended video processing...")
