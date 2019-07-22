from brightnessDetermining import brightnessDiagramRealtime as bdr
import datetime
import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
avergArr = bdr.setup()
counter = 0
while True:
    a = datetime.datetime.now()
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bdr.trueLoop(avergArr, image, False, counter)
    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        break
    b = datetime.datetime.now()
    print("time: " + str(b - a))