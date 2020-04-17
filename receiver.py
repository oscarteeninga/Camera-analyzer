import cv2
import numpy as np
import time
from darkflow.net.build import TFNet
import _thread


options = {"model": "cfg/yolo.cfg", 
           "load": "bin/yolo.weights", 
           "threshold": 0.1, 
           "gpu": 1.0}

tfnet = TFNet(options)

def boxing(original_img, predictions):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']

        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))

        if confidence > 0.3:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
            
    return newImage

step = 0
capture = cv2.VideoCapture('rtsp://admin:10S7r13pe93@192.168.1.105:554')

results = 0

def predict(frame):
    global results
    stime = time.time()
    results = tfnet.return_predict(frame)
    print(time.time() - stime)

while(True):
    ret, frame = capture.read()
    if ret == True:
        frame = np.asarray(frame)
        if step == 0:
            _thread.start_new_thread(predict, (frame, ))
            step = 40
        else:
            step -= 1

        if results:
            new_frame = boxing(frame, results)
        else:
            new_frame = frame
        cv2.imshow('frame',new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


capture.release()
cv2.destroyAllWindows()