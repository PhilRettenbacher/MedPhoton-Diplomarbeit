import cv2
from ImagingApi import ImagingApi
import numpy as np;

#The onboard webcam usually has the id 0
webcamID = 2;
webcamID2 = 1;

cam = ImagingApi.CameraApi(True, (1,2))

cap = cv2.VideoCapture('http://192.168.199.3:808' + str(webcamID) + '/')
cap2 = cv2.VideoCapture('http://192.168.199.3:808' + str(webcamID2) + '/')

# Check success
if not cap.isOpened():
    raise Exception("Could not open video device")
if not cap2.isOpened():
    raise Exception("Could not open video device")

counter = 0;
alpha = 3
beta = -150

while(True):
    # Capture frame-by-frame
    [frame, frame2] = cam.getPicture()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    cv2.convertScaleAbs(frame, frame, alpha, beta);
    cv2.convertScaleAbs(frame2, frame2, alpha, beta);

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('frame2', frame2)

    lv_x = frame.winfo_rootx()
    lv_y = frame.winfo_rooty()
    print (lv_x, lv_y)

    if cv2.waitKey(1) == 32:
        #Right Cam
        cv2.imwrite("image_R_"+str(counter)+".jpg", frame);
        print("Image R taken")

        #Left Cam
        cv2.imwrite("image_L_" + str(counter) + ".jpg", frame2);
        print("Image L taken")

        counter = counter + 1;

    if cv2.waitKey(1) == 27:
        break

cam.__del__()