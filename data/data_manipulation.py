import random
import os
from os.path import isfile, join

mypath = os.path.dirname(os.path.abspath(__file__))
# train_images = mypath + '\\train\\images'
# train_labels = mypath + '\\train\\labels'
# valid_images = mypath + '\\valid\\images'
# valid_labels = mypath + '\\valid\\labels'
# txt = [f for f in os.listdir(valid_images) if isfile(join(valid_images, f)) and "txt" in f]

# # rename files
# for file in txt:
#     print(file)
#     print(valid_images + '\\' + file, valid_labels + '\\' + file)
#     os.rename(valid_images + '\\' + file, valid_labels + '\\' + file)

# Relabel battery labels
b_test_labels = mypath + '/battery/train/labels'
b_test_images = mypath + '/battery/train/images'
b_labels = [f for f in os.listdir(b_test_labels) if isfile(join(b_test_labels, f)) and "txt" in f]
counter = 0
for label in b_labels:
    counter += 1
    # print(label)
    lines = []
    with open(join(b_test_labels, label), "r") as f:
        lines = f.readlines()
    # print(lines)
    if len(lines) == 0:
        print(label)
    for i in range(len(lines)):
        if len(lines[i].split(" ")) != 5:
            print(label)
        lines[i] = "5" + lines[i][1:]
    # print(lines)
    # with open(join(b_test_labels, label), "w") as f:
    #     f.writelines(lines)