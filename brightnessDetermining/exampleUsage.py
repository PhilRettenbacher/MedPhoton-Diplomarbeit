from brightnessDetermining import brightnessDiagramRealtime as bdr
import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
avergArr = bdr.setup()
while True:
    ret, image = cap.read()
    #image = cv2.imread('testpic.jpg')
    bdr.trueLoop(avergArr, image)