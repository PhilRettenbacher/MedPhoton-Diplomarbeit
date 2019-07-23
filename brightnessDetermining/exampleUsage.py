from brightnessDetermining import brightnessDiagramRealtime as bdr
import datetime
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
arrays = bdr.setup()
time = []

counter = 0
while True:
    a = datetime.datetime.now()
    ret, image = cap.read()
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        print('\033[1;31m Input error! No webcam found')
        exit(0)

    bdr.trueLoop(arrays, image, True, counter, 10)
    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        break
    b = datetime.datetime.now()
    print("Berechnungszeit: " + str(b-a))