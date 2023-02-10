# Object Detection Mobile App with Kivy

## Introduction
This project demonstrates how to build a mobile application for object detection using the Kivy framework and TensorFlow Lite. The application utilizes a pre-trained TensorFlow Lite model to perform object detection on an image captured by the device camera.

## Requirements
- Python 3.x
- Kivy
- TensorFlow
- TensorFlow Lite
- onnx

## Convert from ONNX to TFLite
Before running the application, we need to convert the pre-trained ONNX model to TensorFlow Lite format using the `onnx2tflite.py` script. To do this, run the following command:

`
$ python onnx2tflite.py <weight_onnx>
`



## Running the Application
Once the TFLite model has been converted, we can run the object detection application using the following command:

`
$ python search_v3.1.py
`

## Conclusion
This project demonstrates the simplicity and ease of building a mobile object detection application using the Kivy framework and TensorFlow Lite. The application can be easily customized and expanded to perform more advanced tasks.

