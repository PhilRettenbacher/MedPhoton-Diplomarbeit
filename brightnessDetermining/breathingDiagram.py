from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime

class BreathingPlotter:
    def __init__(self, plots, imShape, plotLen):
        self.imShape = imShape
        self.plotLen = plotLen
        self.calc = BreathingCalculater(imShape, plotLen)
        self.plots = plots

        plt.ion()
        styles = ('r-', 'g-', 'y-', 'b-')

        self.fig = plt.figure()
        self.ax = [self.fig.add_subplot(221), self.fig.add_subplot(222), self.fig.add_subplot(223), self.fig.add_subplot(224)]

        self.lines = [0, 0, 0, 0]
        for j, (x) in enumerate(self.ax):
            xV = np.linspace(0, self.calc.data[plots[j].value].shape[0], self.calc.data[plots[j].value].shape[0])
            yV = np.linspace(0, self.calc.data[plots[j].value][0], num=self.calc.data[plots[j].value].shape[0])
            self.lines[j], = x.plot(xV, yV, styles[j])
        #self.line1, = self.ax[0].plot(x, y, 'r-')

    def update(self, img):
        self.calc.update(img)

        for j, line in enumerate(self.lines):
            line.set_ydata(self.calc.data[self.plots[j].value])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(1e-17)

class BreathingCalculater:
    def __init__(self, imShape, plotLen, oldtime = 0):
        self.oldtime = oldtime
        self.imShape = imShape
        self.plotLen = plotLen
        self.data = [np.ones(self.imShape[0])*255,  # AVG_BRIGHT_ROW
                     np.ones(self.imShape[1])*255,  # AVG_BRIGHT_COL
                     np.ones(self.plotLen)*300,     # AVG_BRIGHT_TIME
                     np.ones(self.plotLen)*400,     # WEIGHT_ROW_TIME
                     np.ones(self.plotLen)*550,     # WEIGHT_COL_TIME
                     np.ones(self.plotLen)*1400]    # SUM_TIME
    def fps(self):
        fps = round(1.0 / (float(datetime.datetime.now().strftime('%S.%f')) - self.oldtime), 1)
        self.oldtime = float(datetime.datetime.now().strftime('%S.%f'))
        plt.suptitle('fps: ' + str(fps), fontsize=10)

    def centerOfMass(self, array):
        sum = cv2.sumElems(np.array(array))[0]
        i = 0
        for x in range(len(array)):
            i += array[x]
            if i >= (sum / 2):
                return x

    def prepareAvg(self, img):
        self.data[BreathPlot.AVG_BRIGHT_ROW.value] = np.sum(img, axis=1)/(np.count_nonzero(img, axis=1)+1)
        self.data[BreathPlot.AVG_BRIGHT_COL.value] = np.sum(img, axis=0)/(np.count_nonzero(img, axis=0)+1)

    def getAvg(self):
        self.data[BreathPlot.AVG_BRIGHT_TIME.value] = np.roll(self.data[BreathPlot.AVG_BRIGHT_TIME.value], 1)
        self.data[BreathPlot.AVG_BRIGHT_TIME.value][0] = round(
            cv2.mean(np.array(self.data[BreathPlot.AVG_BRIGHT_ROW.value]))[0])

    def getWeight(self):
        self.data[BreathPlot.WEIGHT_ROW_TIME.value] = np.roll(self.data[BreathPlot.WEIGHT_ROW_TIME.value], 1)
        self.data[BreathPlot.WEIGHT_COL_TIME.value] = np.roll(self.data[BreathPlot.WEIGHT_COL_TIME.value], 1)
        self.data[BreathPlot.WEIGHT_ROW_TIME.value][0] = self.centerOfMass(self.data[BreathPlot.AVG_BRIGHT_ROW.value])
        self.data[BreathPlot.WEIGHT_COL_TIME.value][0] = self.centerOfMass(self.data[BreathPlot.AVG_BRIGHT_COL.value])

    def getSum(self, arrays):
        self.data[BreathPlot.SUM_TIME.value] = np.roll(self.data[BreathPlot.SUM_TIME.value], 1)
        self.data[BreathPlot.SUM_TIME.value] = np.array([sum(x) for x in zip(*[arrays[0], arrays[1], arrays[2]])])

    def update(self, img):
        self.fps()              # calculate fps

        self.prepareAvg(img)    # AVG_BRIGHT_ROW, AVG_BRIGHT_COL
        self.getAvg()           # AVG_BRIGHT_TIME
        self.getWeight()        # WEIGHT_ROW_TIME, WEIGHT_COL_TIME
        self.getSum((           # SUM_TIME
            self.data[BreathPlot.AVG_BRIGHT_TIME.value],
            self.data[BreathPlot.WEIGHT_ROW_TIME.value],
            self.data[BreathPlot.WEIGHT_COL_TIME.value]
        ))


class BreathPlot(Enum):
    AVG_BRIGHT_ROW=0
    AVG_BRIGHT_COL=1
    AVG_BRIGHT_TIME=2
    WEIGHT_ROW_TIME=3
    WEIGHT_COL_TIME=4
    SUM_TIME=5

