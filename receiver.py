import cv2
import numpy as np
import time
import csv
import repository
from sys import argv

if argv[2] == "tiny":
    print("Launching system for TinyYOLO")
    CONFIG='cfg/yolov3-tiny.cfg'
    WEIGHTS='./bin/yolov3-tiny.weights'
elif argv[2] == "regular":
    print("Launching system for YOLO")
    CONFIG='cfg/yolov3-320.cfg'
    # https://pjreddie.com/media/files/yolov3.weights
    WEIGHTS='./bin/yolov3-320.weights'
else:
    print("Unkown model")

capture = cv2.VideoCapture('rtsp://admin:camera123@192.168.1.125:554')
net = cv2.dnn.readNet(WEIGHTS, CONFIG)

CLASSES='./yolov3.txt'
classes = None
with open(CLASSES, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

scale = 0.00392
conf_threshold = 0.3
nms_threshold = 0.3
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def processImage(image, index, net, size, show=False):
    Width = image.shape[1]
    Height = image.shape[0]

    blob = cv2.dnn.blobFromImage(image, scale*size/416, (size, size), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2

                # save event to database
                label = str(classes[class_id])
                print("Saving event: " + label + " with confidence: " + str(confidence))

                repository.insert(label,str(confidence))
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

    # display output image
    if show:
        out_image_name = "object detection"
        cv2.imshow(out_image_name, image)


def timeTest(size, iteration = 20):
    result = []
    read_time = 0
    process_time = 0
    begin = time.time()
    for _ in range(1, iteration):
        stime = time.time()
        ret, frame = capture.read()
        read_time += time.time() - stime
        if ret == True:
            stime = time.time()
            processImage(frame, 1, net, size)
            process_time += time.time() - stime
    end_time = (time.time() - begin)
    capture.release()
    cv2.destroyAllWindows()
    return [size, end_time/iteration, read_time/iteration, process_time/iteration]

def video(size, iteration = 1000):
    print("Begin presentation...")
    for i in range(1, iteration):
        begin = time.time()
        ret, frame = capture.read()
        if ret == True:
            processImage(frame, 1, net, size, True)
            print(time.time() - begin)
        cv2.waitKey(1)
            
    capture.release()
    cv2.destroyAllWindows()

def test():
    result = []
    sizes = [64, 96, 128, 160, 192, 256, 320, 416]
    for size in sizes:
        result.append(timeTest(size))
        print(size)
    print(result)
    return result

def tests():    
    with open('test.csv', 'w', newline='') as output_file_name:
            writer = csv.writer(output_file_name)
            for result in test():
                writer.writerow(result)
            output_file_name.close()

video(int(argv[1]), 10000)