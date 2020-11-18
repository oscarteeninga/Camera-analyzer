import time

import cv2
import numpy as np
from config.yoloconfig import YoloConfig
from config.cameraconfig import CameraConfig
from config.areaconfig import AreaConfig
from model.receiver import Receiver

from services.areaservice import AreaService
from services.eventservice import EventService

CONSOLE_INFO = 0


class Analyzer:

    def __init__(self, camera_config: CameraConfig, yolo_config=None):
        self.on = True
        self.camera_config = camera_config
        self.yolo_config = yolo_config if yolo_config else YoloConfig.basic()
        self.area_service = AreaService()
        self.event_service = EventService()
        self.capture = Receiver(camera_config)
        self.net = self.yolo_config.net()

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

                    self.area_service.get_areas(self.camera_config.id)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        return boxes, class_ids, confidences

    def show_image(self, image, boxes, class_ids, confidences):

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.yolo_config.conf_threshold, self.yolo_config.nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]

            self.draw_bounding_box(image, class_ids[i], round(x), round(y), round(w), round(h))

        out_image_name = "Analyzer"
        cv2.imshow(out_image_name, image)

    def one_process_episode(self, show):
        frame = self.capture.read()
        begin_time = time.time()
        boxes, class_ids, confidences = self.process_frame(frame)

        if show:
            self.show_image(frame, boxes, class_ids, confidences)

        if CONSOLE_INFO == 1:
            print("Process time: " + str(time.time()-begin_time))
        cv2.waitKey(1)

    def video(self, show=False):

        if CONSOLE_INFO == 1:
            print("Begin video processing...")

        while self.on:
            self.one_process_episode(show)

        print("Ended video processing...")
