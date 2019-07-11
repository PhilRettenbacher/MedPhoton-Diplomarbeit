import cv2
import numpy as np

webcamID = 1;
cap = cv2.VideoCapture('http://192.168.199.3:808' + str(webcamID) + '/')
# mouse callback function
def getCoords(event,x,y,flags,param):
    print(x,y)

while(1):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getCoords)
    cv2.imshow('image',frame)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()