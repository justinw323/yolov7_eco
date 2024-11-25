import serial
import time
import os
import detect_script as script
import live_capture as capture
import send_data 

port="/dev/ttyACM0"

arduino = serial.Serial(port, baudrate=9600, timeout=1)
done = False

while not done:
	data = arduino.readline()
	if data:
		print(data)
		if data == b'\x01':
			# capture.show_camera()
			os.system("gst-launch-1.0 nvarguscamerasrc num-buffers=1 sensor_id=0 ! 'video/x-raw(memory:NVMM), width=4608, height=2592, framerate=14/1, format=NV12' ! nvjpegenc ! filesink location=image.jpg")
			label, isRecyclable = script.detect("capture.jpg")
			arduino.write(str(int(isRecyclable)).encode())
			arduino.flush()
			done = True
			#send_data.get_data(label, isRecyclable)
			print(label, isRecyclable)
	else:
		print("no data")
	time.sleep(5)

arduino.close() 
