import datetime
import json
import serial
import cv2
import time

import ecosort_detect

classes = {'Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic'}
port="/dev/ttyACM0"

def parse_labels(labels):
    if len(labels) > 0: # Take the first label for web app
        if labels[0][0] in classes and labels[0][1] > 0.85:
            return labels[0][0], True
    return "Trash", False

def save_to_json(item_data):
    date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day).isocalendar()
    json_file_path = "recycling_data.json"
    data = {
		"label": item_data[0],
		"category": item_data[1],
		"year": datetime.datetime.now().year,
		"week": date.week,
		"weekday": date.weekday,
		"hour": datetime.datetime.now().hour
	}
    try: 
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            if "data" not in existing_data or not isinstance(existing_data["data"], list):
                raise ValueError("Existing json data is of incorrect format")
    except FileNotFoundError:
        existing_data = {data: []}
    
    existing_data["data"].append(data)
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)\

if __name__ == '__main__':
    # Arduino + camera initalization
    arduino = serial.Serial(port, baudrate=9600, timeout=1)
    done = False
    cam = cv2.VideoCapture(0)
    #Check if camera was opened correctly
    if not (cam.isOpened()):
        print("Could not open video device")
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    time.sleep(0.1)
    arduino.read_all()

    # Wait for data from arduino
    while not done:
        data = arduino.readline()
        if data:
            print(data)
            _, frame = cam.read()
            if data == b'\x01':
                cv2.imwrite("capture.jpg", frame)       # take picture

                labels = ecosort_detect.detect()        # run inference, get labels
                webapp_data = parse_labels(labels)      # determine if we should recycle
                save_to_json(webapp_data)               # save data to json storage

                label, isRecyclable = webapp_data
                arduino.write(str(int(isRecyclable)).encode())
                arduino.flush()
                done = True
                print(label, isRecyclable)
        else:
            print("no data")
        time.sleep(5)

    

    # labels = ecosort_detect.detect()        # run inference, get labels
    # print(labels)
    # webapp_data = parse_labels(labels)      # determine if we should recycle
    # print(webapp_data)
    # save_to_json(webapp_data)               # save data to json sotrage