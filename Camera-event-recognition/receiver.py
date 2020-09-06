import cv2
import numpy as np
import time
import csv
import repository
import threading
from sys import argv

class CameraConfig:
    def __init__(self, camera_ip, camera_user, camera_password):
        self.capture = cv2.VideoCapture('rtsp://' + camera_user + ':' + camera_password+ '@' + camera_ip + ':554')
        b = time.time()
        print("Checking FPS...")
        for _ in range(150):
            self.capture.read()
        self.fps = int(150/(time.time()-b))
        print("FPS set on: " + str(self.fps))

    def set_fps(self, fps):
        self.fps = fps

class YoloConfig:
    def __init__(self, weights_file, classes_file, config_file, batch_size):
        self.classes_file = classes_file
        self.config_file = config_file
        self.weights_file = weights_file
        self.batch_size = batch_size

        self.scale = 0.00392
        self.conf_threshold = 0.3
        self.nms_threshold = 0.3

        self.classes = None
        with open(self.classes_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.net = cv2.dnn.readNet(self.weights_file, self.config_file)

class CameraAnalyzer:

    def __init__(self, camera_config, yolo_config):
        self.camera_config = camera_config
        self.yolo_config = yolo_config

    def get_output_layers(self):
        layer_names = self.yolo_config.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.yolo_config.net.getUnconnectedOutLayers()]
        return output_layers

    def draw_bounding_box(self, image, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(self.yolo_config.classes[class_id])
        color = self.yolo_config.colors[class_id]
        cv2.rectangle(image, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(image, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    def process_frame(self, image, index, repository):
        width = image.shape[1]
        height = image.shape[0]

        blob = cv2.dnn.blobFromImage(
            image, self.yolo_config.scale, 
            (self.yolo_config.batch_size, self.yolo_config.batch_size), 
            (0, 0, 0), True, crop=False)
            
        self.yolo_config.net.setInput(blob)
        outs = self.yolo_config.net.forward(self.get_output_layers())

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

                    # save event to database
                    label = str(self.yolo_config.classes[class_id])

                    if repository:
                        repository.insert(label,str(confidence))

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

            self.draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

        out_image_name = "Analyzer"
        cv2.imshow(out_image_name, image)


    def skip_frames(self):
        for _ in range(self.frames_per_process-1):
            self.camera_config.capture.read()


    def one_process_episode(self, repository, show):
        self.skip_frames()
        ret, frame = self.camera_config.capture.read()
        if ret:
            begin_time = time.time()
            boxes, class_ids, confidences = self.process_frame(frame, 1, repository)
            process_time = 1.25*(time.time() - begin_time)/self.frames_per_process

            if process_time > 1.0/self.camera_config.fps:
                self.frames_per_process += int(process_time*self.camera_config.fps)
            else:
                if self.frames_per_process > 1:
                    self.frames_per_process -= 1
            if show:
                self.show_image(frame, boxes, class_ids, confidences)

            print("\tExpected time: " + str(1.0/self.camera_config.fps) + ", Actual time: " + str(process_time) + ", Frames per process:  " + str(self.frames_per_process) + ", Frames per second: " + str(self.camera_config.fps))
        cv2.waitKey(1)


    def video(self, repository=False, show=False):
        self.frames_per_process = 1

        print("Begin video proccessing...")
        while True:
            self.one_process_episode(repository, show)
                
        self.camera_config.capture.release()
        cv2.destroyAllWindows()

cameraConfig = CameraConfig("192.168.1.125", "admin", "camera123")
yoloConfig = YoloConfig("bin/yolov3.weights", "yolov3.txt", "cfg/yolov3.cfg", int(argv[1]))
cameraAnalyzer = CameraAnalyzer(cameraConfig, yoloConfig)

cameraAnalyzer.video(False, True)


