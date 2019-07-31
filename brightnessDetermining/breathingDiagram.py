from scipy.ndimage.filters import gaussian_filter1d
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime

class BreathingPlotter:
    def __init__(self, plots, imShape, plotLen = 100, smooth = True, frequency = 1, autoscale = True):
        self.imShape = imShape
        self.plotLen = plotLen
        self.calc = BreathingCalculater(imShape, plotLen)
        self.plots = plots
        self.frequency = frequency
        self.counter = 0
        self.smooth = smooth
        self.autoscale = autoscale
        ylabels = ['Brightness', 'Brightness', 'Brightness', 'Pixelrow', 'Pixelcolumn', 'Sum']
        xlabels = ['Row', 'Column', 'Time', 'Time', 'Time', 'Time']
        titles = ['Brightness/Row', 'Brightness/Column', 'Brightness/Time', 'RowWeight/Time', 'ColumnWeight/Time', 'Sum/Time']
        ybottomLims = [0, 0, 0, 50, 100, 200]
        ytopLims = [300, 300, 300, 400, 550, 1200]

        plt.ion()
        styles = ('c-', 'y-', 'r-', 'm-', 'b-', 'k-')

        self.fig = plt.figure()
        self.ax = [self.fig.add_subplot(221), self.fig.add_subplot(222), self.fig.add_subplot(223), self.fig.add_subplot(224)]
        plt.tight_layout(pad=2.5, w_pad=1.7, h_pad=2.5)
        self.lines = [0, 0, 0, 0]
        for j, (x) in enumerate(self.ax):
            xV = np.linspace(0, self.calc.data[plots[j].value].shape[0], self.calc.data[plots[j].value].shape[0])
            yV = np.linspace(0, self.calc.data[plots[j].value][0], num=self.calc.data[plots[j].value].shape[0])
            self.lines[j], = x.plot(xV, yV, styles[plots[j].value])
            self.ax[j].set_title(titles[plots[j].value], fontsize=10, fontweight='bold')
            self.ax[j].set_xlabel(xlabels[plots[j].value], fontsize=9)
            self.ax[j].set_ylabel(ylabels[plots[j].value], fontsize=9)
            self.ax[j].spines['right'].set_visible(False)
            self.ax[j].spines['top'].set_visible(False)
            self.ax[j].tick_params(direction='in', length=2, labelsize=8)
            self.ax[j].set_xlim(len(self.calc.data[plots[j].value]), 0)
            self.ax[j].set_ylim(ybottomLims[plots[j].value], ytopLims[plots[j].value])

    def update(self, img):
        self.calc.update(img)
        self.counter += 1

        for j, line in enumerate(self.lines):
            array = self.calc.data[self.plots[j].value]
            if self.autoscale:
                self.ax[j].set_ylim(min(self.calc.data[self.plots[j].value])-50, max(self.calc.data[self.plots[j].value])+50)
            if self.smooth:
                array = gaussian_filter1d(array, sigma=1.5)
            line.set_ydata(array)

        if self.counter%self.frequency == 0:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            plt.pause(1e-17)
        # 0.32 sec

class BreathingCalculater:
    def __init__(self, imShape, plotLen, oldtime = 0):
        self.oldtime = oldtime
        self.imShape = imShape
        self.plotLen = plotLen
        self.data = [np.ones(self.imShape[0]),  # AVG_BRIGHT_ROW
                     np.ones(self.imShape[1]),  # AVG_BRIGHT_COL
                     np.ones(self.plotLen)*-5,  # AVG_BRIGHT_TIME
                     np.ones(self.plotLen),     # WEIGHT_ROW_TIME
                     np.ones(self.plotLen),     # WEIGHT_COL_TIME
                     np.ones(self.plotLen)]     # SUM_TIME
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
        # 0.004 sec


class BreathPlot(Enum):
    AVG_BRIGHT_ROW = 0
    AVG_BRIGHT_COL = 1
    AVG_BRIGHT_TIME = 2
    WEIGHT_ROW_TIME = 3
    WEIGHT_COL_TIME = 4
    SUM_TIME = 5
