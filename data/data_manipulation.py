import random
import os
from os.path import isfile, join

mypath = os.path.dirname(os.path.abspath(__file__))
train_images = mypath + '\\train\\images'
train_labels = mypath + '\\train\\labels'
valid_images = mypath + '\\valid\\images'
valid_labels = mypath + '\\valid\\labels'
txt = [f for f in os.listdir(valid_images) if isfile(join(valid_images, f)) and "txt" in f]

for file in txt:
    print(file)
    print(valid_images + '\\' + file, valid_labels + '\\' + file)
    os.rename(valid_images + '\\' + file, valid_labels + '\\' + file)
