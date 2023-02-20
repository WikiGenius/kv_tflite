# Import packages
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from utils import Detector, resize

Builder.load_file('searchv3.1.kv')
Window.size = (350, 600)

class SearchDashboard(BoxLayout):
    pass

class SearchApp(App):
    def build(self):
        Window.clearcolor=(0,0,0.2)
        self.search = SearchDashboard()
        vid_path = './assets/videos/video2.mp4'
        self.capture = cv2.VideoCapture(vid_path)
        # load model
        self.detector = Detector('./assets/weights/yolov6n_model.tflite').start()

        self.fps = 0
        self.frame_count = 0
        # text input variable
        self.filter_classes = None
        
        Clock.schedule_interval(self.update, 1/33)
        return self.search
    
    def update_search(self):
        self.filter_classes = self.search.text_input.text
        if self.filter_classes:
            self.filter_classes = self.filter_classes.split(',')

    def on_stop(self):
        self.detector.stop()    
        
    def update(self, *args):
        ret, frame = self.capture.read()
        if not ret:
            self.detector.stop()
            return
        frame = resize(frame, width=600)
        
        frame =  self.detector.detect(frame,  conf_thres=0.25, iou_thres=0.45, frame_count=self.frame_count, skip_frame = 1, filter_classes=self.filter_classes)
        
        buf = cv2.flip(frame, 0).tobytes()
        img_texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.search.image.texture = img_texture
        
        self.frame_count +=1

if __name__ == '__main__':
    SearchApp().run()
