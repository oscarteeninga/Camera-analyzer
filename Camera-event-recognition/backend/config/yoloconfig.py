import cv2
import numpy as np


class YoloConfig:
    def __init__(self, batch_size,
                 weights_file="bin/yolov3.weights",
                 classes_file="yolov3.txt",
                 config_file="cfg/yolov3.cfg"):
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
