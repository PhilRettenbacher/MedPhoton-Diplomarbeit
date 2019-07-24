from brightnessDetermining import brightnessDiagramRealtime as bdr
import datetime
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
arrays = bdr.setup()
time = []

counter = 0
while True:
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    a = datetime.datetime.now()
    bdr.trueLoop(arrays, image, True, counter, 1, True, True, True, True)
    b = datetime.datetime.now()
    print("Berechnungszeit: " + str(b - a))
    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        exit(0)
