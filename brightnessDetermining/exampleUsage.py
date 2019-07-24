from brightnessDetermining import brightnessDiagramRealtime as bdr
import datetime
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
arrays = bdr.setup()
time = []

counter = 0
sec = 0
while True:
    a = datetime.datetime.now().strftime('%S.%f')
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    bdr.trueLoop(arrays, sec, image, True, counter, 1, True, True, True, True)


    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        exit(0)
    b = datetime.datetime.now().strftime('%S.%f')
    sec = float(b)-float(a)
    #print(str(sec) + " seconds")
