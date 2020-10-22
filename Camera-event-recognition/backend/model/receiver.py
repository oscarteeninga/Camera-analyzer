import cv2
import numpy as np
import time

CONSOLE_INFO = 1


class DetectBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.width = width
        self.y = y
        self.height = height

    def field(self, a, b):
        if min(a, b) < 0:
            return 0
        else:
            return a * b

    def coverage(self, x, y, width, height):
        x1 = max(self.x, x)
        y1 = max(self.y, y)
        x2 = min(self.x + self.width, x + width)
        y2 = min(self.y + self.height, y + height)
        common_width = (x2 - x1)
        common_height = (y2 - y1)
        return self.field(common_width, common_height) / self.field(width, height)


class CameraAnalyzer:

    def __init__(self, configuration, repository=None):
        self.frames_per_process = 1
        self.camera_config = configuration.camera_config
        self.yolo_config = configuration.yolo_config
        self.repository = repository
        self.detect_box = None
        self.fps = self.camera_config.fps

    def set_detect_box(self, detect_box):
        self.detect_box = detect_box

    def get_output_layers(self):
        layer_names = self.yolo_config.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.yolo_config.net.getUnconnectedOutLayers()]
        return output_layers

    def draw_bounding_box(self, image, class_id, x, y, x_plus_w, y_plus_h):
        label = str(self.yolo_config.classes[class_id])
        color = self.yolo_config.colors[class_id]
        cv2.rectangle(image, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(image, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def process_frame(self, image, store):
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

                    if self.detect_box and self.detect_box.coverage(x, y, w, h) < 0.3:
                        continue

                    label = str(self.yolo_config.classes[class_id])

                    if store and self.repository:
                        self.repository.insert(label, str(confidence), x, y, w, h)

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

            self.draw_bounding_box(image, class_ids[i], round(x), round(y), round(x + w), round(y + h))

        if self.detect_box:
            self.draw_bounding_box(image, 80, self.detect_box.x, self.detect_box.y,
                                   self.detect_box.x + self.detect_box.width,
                                   self.detect_box.y + self.detect_box.height)

        out_image_name = "Analyzer"
        cv2.imshow(out_image_name, image)

    def skip_frames(self):
        for _ in range(self.frames_per_process - 1):
            self.camera_config.capture.read()

    def update_frames_per_process(self, begin_time):
        process_time = 1.25 * (time.time() - begin_time) / self.frames_per_process

        if process_time > 1.0 / self.fps:
            self.frames_per_process += int(process_time * self.fps)
        else:
            if self.frames_per_process > 1:
                self.frames_per_process -= 1

        return process_time

    def one_process_episode(self, repository, show):
        self.skip_frames()
        ret, frame = self.camera_config.capture().read()
        if ret:
            begin_time = time.time()
            boxes, class_ids, confidences = self.process_frame(frame, repository)

            process_time = self.update_frames_per_process(begin_time)

            if show:
                self.show_image(frame, boxes, class_ids, confidences)

            if CONSOLE_INFO == 1:
                print(
                    "\tExpected time: " + str(round(1.0 / self.fps, 3)) + " s"
                    ", Actual time: " + str(round(process_time, 3)) + " s"
                    ", Frames per process:  " + str(self.frames_per_process) +
                    ", Frames per second: " + str(self.fps)
                )
        cv2.waitKey(1)

    def video(self, repository=False, show=False):

        if CONSOLE_INFO == 1:
            print("Begin video processing...")

        while True:
            self.one_process_episode(repository, show)
