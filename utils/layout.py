# Import necessary packages
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import cv2
import os

# Load the Kivy file
Builder.load_file('searchv3.1.kv')

# Define a custom widget for loading files
class LoadFile(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# Define the main widget for the app
class SearchDashboard(BoxLayout):
    pass
