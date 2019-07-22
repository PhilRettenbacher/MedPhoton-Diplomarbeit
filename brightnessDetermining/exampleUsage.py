from brightnessDetermining import brightnessDiagramRealtime as bdr
import datetime
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
avergArr = bdr.setup()
time = []

counter = 0
while True:
    a = datetime.datetime.now()
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bdr.trueLoop(avergArr, image, True, counter, 1, 3, True)
    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        break
    b = datetime.datetime.now()
    #print("Berechnungszeit: " + str(b-a))