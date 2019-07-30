from brightnessDetermining import brightnessDiagramRealtime
import datetime
import cv2

bdr = brightnessDiagramRealtime.BrightnessDiagramRealtime()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time = []

counter = 0
sec = 0
while True:
    timeStart = datetime.datetime.now().strftime('%S.%f')
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bdr.trueLoop(counter, image, frequency=1, scaling=False, arr1=True, arr2=True, arr3=True)
    counter += 1

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        exit(0)
    timeEnd = datetime.datetime.now().strftime('%S.%f')
    sec = float(timeEnd)-float(timeStart)
    #print(str(round(sec, 2)) + " seconds")
