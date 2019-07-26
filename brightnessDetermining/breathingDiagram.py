from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

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
            print(plots[j].value)
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
        plt.pause(0.0001)

class BreathingCalculater:
    def __init__(self, imShape, plotLen):
        self.imShape = imShape
        self.plotLen = plotLen
        self.data = [np.ones(self.imShape[0])*255,
                     np.ones(self.imShape[1])*255,
                     np.ones(self.imShape[0]),
                     np.ones(self.imShape[1]),
                     np.ones(self.plotLen),
                     np.ones(self.plotLen),
                     np.ones(self.plotLen),
                     np.ones(self.plotLen),
                     np.ones(self.plotLen)]

    def prepareAvg(self, img):
        self.data[BreathPlot.AVG_BRIGHT_ROW] = np.sum(img, axis=1)/(np.count_nonzero(img, axis=1)+1)
        self.data[BreathPlot.AVG_BRIGHT_COL] = np.sum(img, axis=0)/(np.count_nonzero(img, axis=0)+1)

    def update(self, img):
        self.prepareAvg(img)

class BreathPlot(Enum):
    AVG_BRIGHT_ROW=0
    AVG_BRIGHT_COL=1
    AVG_BRIGHT_ROW_TIME=2
    AVG_BRIGHT_COL_TIME=3
    WEIGHT_ROW_TIME=4
    WEIGHT_COL_TIME=5
    SUM_TIME=6

