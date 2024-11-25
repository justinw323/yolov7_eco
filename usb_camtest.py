# https://developer.ridgerun.com/wiki/index.php/How_to_Capture_Frames_from_Camera_with_OpenCV_in_Python
# ^ code from here

import cv2

# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
cap = cv2.VideoCapture(0)

#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")


#Set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Capture frame-by-frame
while(True):
    ret, frame = cap.read()

    # Display the resulting frame
    
    cv2.imshow("preview",frame)
    
    # Uncomment this line if you want a jpg to be a webcam
    # cv2.imwrite("outputImage.jpg", frame)

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()