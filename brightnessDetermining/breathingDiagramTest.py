from brightnessDetermining.breathingDiagram import BreathingPlotter
from brightnessDetermining.breathingDiagram import BreathPlot
import cv2

img = cv2.imread("testpic.jpg")
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#cv2.imshow("a", img)
#cv2.waitKey(0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, image = cap.read()
diagram = BreathingPlotter((BreathPlot.AVG_BRIGHT_TIME, BreathPlot.SUM_TIME, BreathPlot.WEIGHT_COL_TIME, BreathPlot.WEIGHT_ROW_TIME), image.shape, 100)

while True:
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    diagram.update(image)