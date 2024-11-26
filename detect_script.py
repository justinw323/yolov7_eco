import argparse
import time
from pathlib import Path
import os

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
from live_capture import show_camera



def detect(image_path, save_img=False):
    source, weights, imgsz, trace = image_path, "./trashnet50best.pt", 640, True
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))


    # Initialize
    set_logging()
    device = select_device("0")       # 0 = gpu
    # device = select_device("")      # If cuda isn't working, have to use cpu
    half = device.type != 'cpu'  # half precision only supported on CUDA
    print(device.type)        # device.type = cuda

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    if trace:
        model = TracedModel(model, device, 640)
    
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        print('classify')
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()
    # Set Dataloader
    vid_path, vid_writer = None, None
    # while True:
    #     if os.path.isfile("capture.jpg"):
    #         break
    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
            
    recycleable = True
    label = ""

    for path, img, im0s, vid_cap in dataset:
        print("Starting detection on image", path)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=False)[0]

        # Inference
        t1 = time_synchronized()
        with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
            pred = model(img, augment=False)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)		# 0.25 = confidence threshold
        t3 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)
        
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
		
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    recycleable = recycleable and (int(cls) in [0,1,2,3,4] and float(conf) > 0.6)
                    print("Detected cls", f'{names[int(cls)]}', "with conf", f'{conf:.2f}')
                    if label == "":
                        label = names[int(cls)]

            # Print time (inference + NMS)
            print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
    if label == "":
        label = "Trash"
        recycleable = False
        print("No recycling detected")
    print(f'Done. ({time.time() - t0:.3f}s)')
    if not recycleable:
        label = "Trash"
    return label, recycleable


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='capture.jpg', help='source')  # file/folder, 0 for webcam
    opt = parser.parse_args()
    #check_requirements(exclude=('pycocotools', 'thop'))

    with torch.no_grad():
        output = detect(opt.source)
        # output = detect(some path here)
        print("Classification:", output[0], "\tisRecycleable:", output[1])

'''zzzzzzzzzzzzzzz
python3 detect.py --weights trashnet50best.pt --conf 0.25 --img-size 640 --source data/trashnet_test/images/metal153_jpg.rf.3009fa8073f8f28688e8b3f08381d60d.jpg --device=0
python3 detect.py --weights trashnet50best.pt --conf 0.25 --img-size 640 --source capture.jpg --device=0
python3 detect_script.py
python3 detect_script.py --source plastic_demo.jpg
python3 detect_script.py --source trash_demo.jpg
'''

'''
Need to install pytorch and torchvision
https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
When you get to this step:
$ python3 setup.py install --user
do not include --user flag
'''