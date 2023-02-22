# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

# Import necessary libraries
from threading import Thread
from utils import draw_boxes, get_model, preprocess
import time
import cv2

# Define the Detector class
class Detector:
    def __init__(self, model_tflite_path, use_cuda=False):
        # Initialize variables
        self.use_cuda = use_cuda
        self.model, self.input_details, self.output_details = get_model(model_tflite_path)
        self.input_shape = self.input_details[0]['shape'][2:]
        self.output_data = []
        self.stopped = True # Variable to control when model is stopped
        self.detect_started = False
        self.thread_detect = False

        
    def start(self):
        # Start the thread that update_detection
        self.thread_detect = True
        Thread(target=self.update_detection, args=(), daemon=True).start()
        return self


    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True

        
    def update_detection(self):
        while True:
            if not self.stopped:
                self.detection_process()

                    
    def detection_process(self):
        if self.frame_count % self.skip_frame == 0:
            prevTime = time.time()
            im,  self.ratio, self.dwdh = preprocess(self.img, self.input_shape)
            # predict the model
            self.model.set_tensor(self.input_details[0]['index'], im)
            self.model.invoke()
            self.output_data = self.model.get_tensor(self.output_details[0]['index'])
            currTime = time.time()
            self.fps = 1 / (currTime - prevTime)
            self.detect_started = True

            
    def detect(self, img, conf_thres=0.25, iou_thres=0.45, frame_count=0, skip_frame=10, filter_classes=None):
        self.img = img
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.frame_count = frame_count
        self.skip_frame = skip_frame
        self.filter_classes = filter_classes
        self.stopped = False
        if not self.thread_detect:
            self.detection_process()
        else:
            # time.sleep(0.02)
            pass
            
        if self.detect_started :
            img = draw_boxes(img, self.ratio, self.dwdh, self.output_data,
                             conf_thres, filter_classes=filter_classes)
            if not self.thread_detect:
                cv2.line(img, (20, 25), (127, 25), [85, 45, 255], 30)
                cv2.putText(img, f'FPS: {int(self.fps)}', (11, 35), 0, 1, [
                    225, 255, 255], thickness=2, lineType=cv2.LINE_AA)

        return img

