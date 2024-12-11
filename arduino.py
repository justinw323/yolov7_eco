import serial
import time
import os
import cv2

from camera_capture import Camera
import detect_script as script
# import live_capture as capture
import send_data 

port="/dev/ttyACM0"

# General initalization
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

while not done:
	data = arduino.readline()
	if data:
		print(data)
		_, frame = cam.read()
		if data == b'\x01':
			cv2.imwrite("capture.jpg", frame)
			# capture.show_camera()
			# os.system("gst-launch-1.0 nvarguscamerasrc num-buffers=1 sensor_id=0 ! 'video/x-raw(memory:NVMM), width=4608, height=2592, framerate=14/1, format=NV12' ! nvjpegenc ! filesink location=image.jpg")
			label, isRecyclable = "label", 0 #script.detect("capture.jpg")
			arduino.write(str(int(isRecyclable)).encode())
			arduino.flush()
			done = True
			#send_data.get_data(label, isRecyclable)
			print(label, isRecyclable)
	else:
		print("no data")
	time.sleep(5)

arduino.close() 
