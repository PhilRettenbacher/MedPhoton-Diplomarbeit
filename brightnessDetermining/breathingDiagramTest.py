from brightnessDetermining.breathingDiagram import BreathingPlotter
from brightnessDetermining.breathingDiagram import BreathPlot
import matplotlib.pyplot as plt
import cv2

img = cv2.imread("imageFrame_0_0.jpg")
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow("a", img)
cv2.waitKey(0)
diagram = BreathingPlotter((BreathPlot.AVG_BRIGHT_ROW, BreathPlot.AVG_BRIGHT_COL, BreathPlot.SUM_TIME, BreathPlot.WEIGHT_ROW_TIME), img.shape, 100)

for x in range(0, 100):
    diagram.update(img)