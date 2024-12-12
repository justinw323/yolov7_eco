from trt_utils.utils import preproc, vis
from trt_utils.utils import BaseEngine
import numpy as np
import cv2
import time
import os
import argparse
import datetime

class Predictor(BaseEngine):
    def __init__(self, engine_path):
        super(Predictor, self).__init__(engine_path)
        self.n_classes = 5  # your model classes

def detect():

    starttime = datetime.datetime.now()

    pred = Predictor(engine_path="full30.trt")
    img_path = "capture.jpg"
    if img_path:
      labels = pred.ecosort_inference(img_path, conf=0.1, end2end=True)
      print("Overall time =", datetime.datetime.now() - starttime)
      return labels

if __name__ == '__main__':
    detect()

'''
python tensorrt_yolo/ecosort_detect.py 
^from yolov7_eco directory
'''