import os
import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from utils import Detector, resize
from kivy import platform
from utils.layout import *
from utils.permissions import *


class SearchApp(App):
    def build(self):
        # Set background color of window
        Window.clearcolor = (0, 0, 0.2)
        self.started = False
        self.thread = True
        self.fps = 5
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        
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
        
    def dismiss_popup(self):
        # Dismiss the file chooser popup
        self._popup.dismiss()

    def show_load(self):
        # Show the file chooser popup to load a video
        content = LoadFile(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.7, 0.7))
        self._popup.open()

    def load(self, path, vid_path):
        # Load the selected video file
        print(vid_path)
        print(f"Is the video existed: {os.path.isfile(vid_path)}")
        self.start_app(vid_path, self.fps)
        # Dismiss the file chooser popup
        self.dismiss_popup()
        
    def start_app(self, vid_path, fps=10):
        # Create a video capture object for the selected video file
        self.capture = cv2.VideoCapture(vid_path)
        # Schedule the update function to be called at 33 FPS
        Clock.schedule_interval(self.update, 1/fps)
        # Clock.schedule_once(self.update)

if __name__ == '__main__':
    SearchApp().run()
