from scipy.ndimage.filters import gaussian_filter1d
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime

# BreathingDiagram is a program to get the "breathing curve" visible.
# The main input is a "Disparity Map" where you can see the disparity of an image based on the brightness
# it calculates many different diagrams like the shift of the chest to the top, to the side
# and to the viewers perpective

# Main programmer: Tobias Zwinger


# BreathingPlotter generates the figure, subplots and lines
class BreathingPlotter:

    # plots: transfer 4 plots you want to plot
    #   (e.g. (BreathPlot.WEIGHT_ROW_TIME, BreathPlot.AVG_BRIGHT_TIME, BreathPlot.SUM_TIME, BreathPlot.SIN_CURVE))
    #   recommended: (BreathPlot.WEIGHT_ROW_TIME,
    #                 BreathPlot.WEIGHT_COL_TIME,
    #                 BreathPlot.AVG_BRIGHT_TIME,
    #                 BreathPlot.SUM_TIME)
    # imShape: transfer yourimage.shape to get the height and width of your image
    # plotLen: transfer the length you want your plots to be
    #   recommended: plotLen = 100
    # smooth: if you set smooth to True, your curves will look smoother but less exactly
    #   recommended: smooth = true
    # frequency: if frequenzy = 1, you will update the plot every time the loop restarts,
    #   if frequenzy = 2, the plot will update every second time, and so on.
    #   you can achive more speed the highter your frequency is
    #   recommended: frequenzy = 1
    # autoscale: if autoscale = True, your x axis will scale automaticly, so you will see the whole curve bigger
    #   if autoscale = False, your x achis is fixed to a certain area
    #   recommended: autoscale = True
    def __init__(self, plots, imShape, plotLen = 100, smooth = True, frequency = 1, autoscale = True):
        self.imShape = imShape
        self.plotLen = plotLen
        self.calc = BreathingCalculator(imShape, plotLen)
        self.plots = plots
        self.frequency = frequency
        self.counter = 0
        self.smooth = smooth
        self.autoscale = autoscale

        # Arrays for every plot.
        # ylabels are the labels for the y Axis
        # xlabels are the labels for the x Axis
        # titles are titles
        # the first of each array is for the first diagram. In this case: AVG_BRIGHT_ROW
        # you can see the order of the diagramms in the bottom section of the code
        ylabels = ['Brightness', 'Brightness', 'Brightness', 'Pixelrow', 'Pixelcolumn', 'Sum', ' ']
        xlabels = ['Row', 'Column', 'Time', 'Time', 'Time', 'Time', ' ']
        titles = ['Brightness/Row', 'Brightness/Column', 'Brightness/Time', 'RowWeight/Time', 'ColumnWeight/Time', 'Sum/Time', 'Sin curve']

        # if you set autoscale to False, these are the fixed scalings for each diagram
        # In this case, the diagram AVG_BRIGHT_ROW 's y axis is scales from 0 to 300
        # 0 to 300 is a justified scaling, because the brightness ranges from 0 (black) to 255 (white)
        ybottomLims = [0, 0, 0, 50, 100, 200, -2]
        ytopLims = [300, 300, 300, 400, 550, 1200, 2]

        # the colors and curvestyle of each curve
        # e.g. "c-" is a solid cyan line
        # e.g. "r." would be a dotted red line
        styles = ('c-', 'y-', 'r-', 'm-', 'b-', 'k-', 'k-')

        # create a new figure where we plot our lines
        self.fig = plt.figure()

        # fig.add_subplot will add a diagram to our figure
        # the number inside the bracket was a little complicated to understand at first:
        #   e.g. (221) the first two numbers defines the grid inside the figure
        #   "22" is a 2 by 2 grid, that means we can plot 4 diagrams
        #   the third number "1" is the first diagram, 2 would be the second and so on
        #   e.g. (312) is a 3 by 1 grid (we can plot 3 diagrams) and 2 means this is the second diagram
        # the subplots are called "ax", the first subplot would be self.ax[0]
        self.ax = [self.fig.add_subplot(221), self.fig.add_subplot(222), self.fig.add_subplot(223), self.fig.add_subplot(224)]

        # fix the padding between and around the subplots
        # pad is the padding around the subplots
        # w_pad is the padding between the left-hand-side sublots and the ridht-hand-side subplots
        # h_pad is the padding between the top and the bottom subplots
        plt.tight_layout(pad=2.5, w_pad=1.7, h_pad=2.5)

        # we have 4 lines
        self.lines = [0, 0, 0, 0]

        # for each subplot:
        for j, (x) in enumerate(self.ax):
            # np.linespace returns evenly spaced numbers over a specified interval
            # numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
            # num = numbers of samples to generate
            xV = np.linspace(0, self.calc.data[plots[j].value].shape[0], self.calc.data[plots[j].value].shape[0])
            yV = np.linspace(0, self.calc.data[plots[j].value][0], num=self.calc.data[plots[j].value].shape[0])

            # plots the lines into the ax
            self.lines[j], = x.plot(xV, yV, styles[plots[j].value])

            # for each plot, set title, xlabel, ylabel, xlim, ylim, and some beauty factors
            self.ax[j].set_title(titles[plots[j].value], fontsize=10, fontweight='bold')
            self.ax[j].set_xlabel(xlabels[plots[j].value], fontsize=9)
            self.ax[j].set_ylabel(ylabels[plots[j].value], fontsize=9)
            self.ax[j].spines['right'].set_visible(False)
            self.ax[j].spines['top'].set_visible(False)
            self.ax[j].tick_params(direction='in', length=2, labelsize=8)
            self.ax[j].set_xlim(len(self.calc.data[plots[j].value]), 0)
            self.ax[j].set_ylim(ybottomLims[plots[j].value], ytopLims[plots[j].value])

    # the update function is called every time
    def update(self, img):
        # the calculating has to be done every time too
        self.calc.update(img, self.counter)

        # the counter is nessecary to make the frequency work
        self.counter += 1

        # for each line:
        for j, line in enumerate(self.lines):
            # we update the arrays, we calculated in BreathingCalculator
            array = self.calc.data[self.plots[j].value]

            # if autoscale is activated:
            # self.plots[6] is the "sine-cuve" and it should not be scaled
            if self.autoscale and self.plots[j].value != 6:
                # reset the y scaling
                # "+10" and "-10" is there to get a little distance between the curve's top part
                # and the top of the diagram and between the curve's bottom part and the bottom of the diagram
                # if there's no distance, we would not be able to see the top and bottom part of the curve
                self.ax[j].set_ylim(min(self.calc.data[self.plots[j].value])-10, max(self.calc.data[self.plots[j].value])+10)

            # if smooth is activated:
            if self.smooth and self.plots[j].value != 6:
                # gausssian_filter1d is a special function to smooth a 1d curve
                # scipy.ndimage.gaussian_filter1d(input, sigma, axis=-1, order=0,
                #                                 output=None, mode='reflect', cval=0.0, truncate=4.0)
                # sigma: "standard deviation for Gaussian kernel" how extream should the line be smoothed
                array = gaussian_filter1d(array, sigma=1.5)

            # update the y values of every array
            line.set_ydata(array)

        # Now the frequency comes into play.
        # fig.canvas.draw() claims most of our plotting-time
        # We now only plot every specific time
        # if frequency would be 5, we would only plot every fifth time and reduce our plotting time by a lot
        if self.counter%self.frequency == 0:
            # "Redraw the current figure." We redraw our new calculated arrays
            self.fig.canvas.draw()

            # we have to add a little pause, because otherwise the figure would have no time to plot our lines
            # the figure would calculate and calculate and the whole figure would be grey
            plt.pause(1e-17)

# BreathingCalculator
class BreathingCalculator:
    def __init__(self, imShape, plotLen, oldtime = 0):
        # oldtime is nessecary to calculate the current fps
        self.oldtime = oldtime
        self.imShape = imShape
        self.plotLen = plotLen

        # np.ones returns a new array of given shape and type, filled with ones.
        # numpy.ones(shape, dtype=None, order='C')[source]
        # imShape[0] = height of image
        # imShape[1] = width of image
        self.data = [np.ones(self.imShape[0]),  # AVG_BRIGHT_ROW
                     np.ones(self.imShape[1]),  # AVG_BRIGHT_COL
                     np.ones(self.plotLen)*-5,  # AVG_BRIGHT_TIME
                     np.ones(self.plotLen),     # WEIGHT_ROW_TIME
                     np.ones(self.plotLen),     # WEIGHT_COL_TIME
                     np.ones(self.plotLen),     # SUM_TIME
                     np.ones(self.plotLen)*0]   # SIN_CURVE

    # calculate current fps and show them
    def fps(self):
        fps = round(1.0 / (float(datetime.datetime.now().strftime('%S.%f')) - self.oldtime), 1)
        self.oldtime = float(datetime.datetime.now().strftime('%S.%f'))
        plt.suptitle('fps: ' + str(fps), fontsize=10)

    # calculate the "centerOfMass" of an Array
    # That means we want to find out, on where inside the array are the high values.
    def centerOfMass(self, array):
        # first we sum the whole array
        # cv2.sumElems is much faster than if we would run through the whole array and add everything to a value
        sum = cv2.sumElems(np.array(array))[0]
        i = 0

        # now we run through the whole array and add every number to a value.
        # if the value is the same or bigger than half of the sum, we know the "center of Mass"
        for x in range(len(array)):
            i += array[x]
            if i >= (sum / 2):
                return x

    # determine the brightness of every row and every collumn
    def prepareAvg(self, img):
        # np.sum will sum array elements over a given axis
        # numpy.sum(a, axis=None, dtype=None, out=None, keepdims=<no value>, initial=<no value>, where=<no value>)
        # axis=1 are the rows
        self.data[BreathPlot.AVG_BRIGHT_ROW.value] = np.sum(img, axis=1)/(np.count_nonzero(img, axis=1)+1)
        # axis=0 are the collumns
        self.data[BreathPlot.AVG_BRIGHT_COL.value] = np.sum(img, axis=0)/(np.count_nonzero(img, axis=0)+1)

    # now that we know the average brightness of every row and collumn, we can get the average brightness of the
    # whole image. We save every "AverageBrightnessValue" inside an array and "roll" the array. That means, we
    # shift every value inside the array one position back. The first one will be the second, the second the third
    # and so on. Every time, the first position 0 will be calculated new, and the last postition will be deleted
    def getAvg(self):
        # Roll array elements along a given axis
        # numpy.roll(a, shift, axis=None)
        self.data[BreathPlot.AVG_BRIGHT_TIME.value] = np.roll(self.data[BreathPlot.AVG_BRIGHT_TIME.value], 1)

        # cv2.mean calculates an average (mean) of array elements
        # cv2.mean(src[, mask])
        self.data[BreathPlot.AVG_BRIGHT_TIME.value][0] = round(
            cv2.mean(np.array(self.data[BreathPlot.AVG_BRIGHT_ROW.value]))[0])

    # with the "centerOfMass" function, we can calculate the center of Mass. Then, we do the same,
    # like in the example aboth.
    # We roll the array, and the first postition 0 will be the new calculated "centerOfMass"
    # We calculate both, the center of rows, and collumns
    def getWeight(self):
        self.data[BreathPlot.WEIGHT_ROW_TIME.value] = np.roll(self.data[BreathPlot.WEIGHT_ROW_TIME.value], 1)
        self.data[BreathPlot.WEIGHT_COL_TIME.value] = np.roll(self.data[BreathPlot.WEIGHT_ROW_TIME.value], 1)
        self.data[BreathPlot.WEIGHT_ROW_TIME.value][0] = self.centerOfMass(self.data[BreathPlot.AVG_BRIGHT_ROW.value])
        self.data[BreathPlot.WEIGHT_COL_TIME.value][0] = self.centerOfMass(self.data[BreathPlot.AVG_BRIGHT_COL.value])

    # For the "sum curve" we sum every line over time. This curve does not show much, but
    # WEIGHT_ROW_TIME, WEIGHT_ROW_TIME and AVG_BRIGHT_TIME are included
    def getSum(self, arrays):
        self.data[BreathPlot.SUM_TIME.value] = np.array([sum(x) for x in zip(*[arrays[0], arrays[1], arrays[2]])])

    # The "sine curve" trys to get a sine wave from a given array. We look for the point, the original curve cuts it's
    # average, and store this point into an array. Then we look for the next time the curve cuts its average and then
    # we create a sinecurve between the two points.
    def getSin(self, array):
        # first, find the average
        averg = round(cv2.mean(array)[0])
        arr = []

        # now we run through the array and every time the following value is abouth the average and the current
        # value is below, we define this position as a cut. if this happens again, we create a sine curve between
        # the two points.
        for x in range(len(array)-1):
            if array[x] <= averg and array[x+1] > averg:
                start = x
                arr.append(start)
        for j in range(len(arr)-1):
            # how long should the wave be?
            length = arr[j+1]+1-arr[j]

            # we create x and y values
            x = np.linspace(np.pi, -np.pi, length)
            y = np.sin(x)

            # we plot the sine waves
            for i in range(length):
                self.data[BreathPlot.SIN_CURVE.value][arr[j]+i] = y[i]

    # this happens every thime
    def update(self, img, counter):  
        # we calculate...
        self.fps()              # ... fps

        self.prepareAvg(img)    # ... AVG_BRIGHT_ROW, AVG_BRIGHT_COL
        self.getAvg()           # ... AVG_BRIGHT_TIME
        self.getWeight()        # ... WEIGHT_ROW_TIME, WEIGHT_COL_TIME
        self.getSum((           # ... SUM_TIME
            self.data[BreathPlot.AVG_BRIGHT_TIME.value],
            self.data[BreathPlot.WEIGHT_ROW_TIME.value],
            self.data[BreathPlot.WEIGHT_COL_TIME.value]
        ))
        # ... SIN_CURVE
        self.getSin(self.data[BreathPlot.AVG_BRIGHT_TIME.value])


class BreathPlot(Enum):
    AVG_BRIGHT_ROW = 0
    AVG_BRIGHT_COL = 1
    AVG_BRIGHT_TIME = 2
    WEIGHT_ROW_TIME = 3
    WEIGHT_COL_TIME = 4
    SUM_TIME = 5
    SIN_CURVE = 6
