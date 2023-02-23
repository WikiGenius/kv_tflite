import os
import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from utils import Detector
from kivy import platform
from plyer import filechooser
from kivy.properties import ListProperty

from utils.layout import *
from utils.permissions import *


class SearchApp(App):
    selection = ListProperty([])
    
    def build(self):
        # Set background color of window
        Window.clearcolor = (0, 0, 0.2)
        self.started = False
        self.thread = True
        self.fps = 5
        if platform == 'android':
            self.fps = 5
            Window.bind(on_resize=hide_landscape_status_bar)
        else:
            self.fps = 30
        # Create instance of SearchDashboard
        self.search = SearchDashboard()
        # Load YOLOv6n model for object detection
        model_path = './assets/weights/yolov6n_model.tflite'
        print(f"Is the model existed: {os.path.isfile(model_path)}")
        if self.thread:
            self.detector = Detector(model_path).start()
        else:
            self.detector = Detector(model_path)
        # Initialize variables for video capture
        self.frame_count = 0
        # Initialize variable for filtering object classes
        self.filter_classes = None 
        # Return the instance of SearchDashboard
        return self.search
    
    
    def on_stop(self):
        # Stop the detector when the app is closed
        self.detector.stop()    
        
    def update(self, *args):
        # Read a frame from the video capture device
        ret, frame = self.capture.read()
        # Stop the detector if there are no more frames
        if not ret:
            self.detector.stop()
            return
        # Perform object detection on the frame using the YOLOv6n model
        frame =  self.detector.detect(frame,  conf_thres=0.25, iou_thres=0.45, frame_count=self.frame_count, skip_frame = 1, filter_classes=self.filter_classes)
        if self.thread:
            cv2.line(frame, (20, 25), (127, 25), [85, 45, 255], 30)
            cv2.putText(frame, f'FPS: {int(self.fps)}', (11, 35), 0, 1, [
                    225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
        # Flip the frame vertically for display purposes
        buf = cv2.flip(frame, 0).tobytes()
        # Create a Kivy Texture from the frame
        
        if platform == 'android':
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            
        else:
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            

        # Update the image in SearchDashboard with the new frame
        self.search.image.texture = img_texture
        # Increment frame count
        self.frame_count += 1
        # Clock.schedule_once(self.update)
        
    def update_search(self):
        # Update the filter_classes variable based on the text input in SearchDashboard
        self.filter_classes = self.search.text_input.text
        if self.filter_classes:
            self.filter_classes = self.filter_classes.split(',')    
    
    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filters = ['*.mp4']  # add more video file extensions here
        filechooser.open_file(filters=filters, on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        if selection is not None:
            self.selection = selection

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        vid_path = self.selection[0]
        self.start_app(vid_path, self.fps) 

        
    def start_app(self, vid_path, fps=10):
        # Create a video capture object for the selected video file
        print(f'load file: {vid_path}')
        print(f'file exist: {os.path.isfile(vid_path)}')
        self.capture = cv2.VideoCapture(vid_path)
        # Schedule the update function to be called at 33 FPS
        Clock.schedule_interval(self.update, 1/fps)
        # Clock.schedule_once(self.update)

if __name__ == '__main__':
    SearchApp().run()
