from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cv2


class BrightnessDiagramRealtime:
    def __init__(self):
        self.oldtimeF = 0
        self.oldtimeP = 0
        self.array1 = np.array([])
        self.array2 = np.array([])
        self.array3 = np.array([])
        plt.ioff()
        plt.figure("YourWindowName", figsize=(15, 12), dpi=50)
        plt.style.use('fivethirtyeight')

    def setplt(self, scaleT, scaleB, title, yLabel, xLabel):
        plt.ylim(top=scaleT)
        plt.ylim(bottom=scaleB)
        plt.title(title)
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)

    def getCenterOfMass(self, arr):
        sum = cv2.sumElems(np.array(arr))[0]
        i = 0
        for x in range(len(arr)):
            i+=arr[x]
            if i >= (sum/2):
                return x

    def trueLoop(self, counter, image, smoothed = True, scaling = False, frequency = 1, arr1 = True, arr2 = True, arr3 = True, arr4 = True):
        fps = round(1.0/(float(datetime.datetime.now().strftime('%S.%f')) - self.oldtimeF), 1)
        self.oldtimeF = float(datetime.datetime.now().strftime('%S.%f'))

        arrayRow = np.sum(image, axis=1)/(np.count_nonzero(image, axis=1)+1)
        arrayCol = np.sum(image, axis=0)/(np.count_nonzero(image, axis=0)+1)

        comR = self.getCenterOfMass(arrayRow)
        comC = self.getCenterOfMass(arrayCol)
        if len(self.array1) < 50:
            self.array1 = np.insert(self.array1, 0, round(cv2.mean(np.array(arrayRow))[0]))
            self.array2 = np.insert(self.array2, 0, comR)
            self.array3 = np.insert(self.array3, 0, comC)
        else:
            self.array1 = np.roll(self.array1, 1)
            self.array2 = np.roll(self.array2, 1)
            self.array3 = np.roll(self.array3, 1)
            self.array1[0] = round(cv2.mean(np.array(arrayRow))[0])
            self.array2[0] = comR
            self.array3[0] = comC

        array4 = np.array([sum(x) for x in zip(*[self.array1, self.array2, self.array3])])
        if counter%frequency == 0:
            secP = float(datetime.datetime.now().strftime('%S.%f')) - self.oldtimeP
            self.oldtimeP = float(datetime.datetime.now().strftime('%S.%f'))
            plotps = round(1.0 / secP, 1)

            array1scal = np.interp(self.array1, (self.array1.min(), self.array1.max()), (-1, +1))
            array2scal = np.interp(self.array2, (self.array2.min(), self.array2.max()), (-1, +1))
            array3scal = np.interp(self.array3, (self.array3.min(), self.array3.max()), (-1, +1))
            array4scal = np.interp(array4, (array4.min(), array4.max()), (-1, +1))
            if scaling:
                self.array1 = array1scal
                self.array2 = array2scal
                self.array3 = array3scal
                array4 = array4scal
                buffer = 2

            else: buffer = 50
            if smoothed:
                arrayRow = gaussian_filter1d(arrayRow, sigma=3)
                arrayCol = gaussian_filter1d(arrayCol, sigma=3)
                self.array1 = gaussian_filter1d(self.array1, sigma=1)
                self.array2 = gaussian_filter1d(self.array2, sigma=1)
                self.array3 = gaussian_filter1d(self.array3, sigma=1)
                array4 = gaussian_filter1d(array4, sigma=2)
            arrayRow = np.around(arrayRow, decimals=2)
            arrayCol = np.around(arrayCol, decimals=2)
            self.array1 = np.around(self.array1, decimals=2)
            self.array2 = np.around(self.array2, decimals=2)
            self.array3 = np.around(self.array3, decimals=2)
            array4 = np.around(array4, decimals=2)

            # print(self.array1, self.array3, self.array2)
            plt.clf()
            plt.suptitle('fps: ' + str(fps) + ' pps: ' + str(plotps), fontsize=16)
            if arr1:
                plt.subplot(221)
                self.setplt(max(self.array1)+buffer, min(self.array1)-buffer, 'Average Brightness/Time', 'Brightness', 'Time')
                plt.xlim(len(self.array1), 0)
                plt.plot(self.array1, 'r', linewidth=2, label='averg. brightness')
                plt.legend(loc=1, fontsize=20)
            if arr2:
                plt.subplot(222)
                self.setplt(400, 100, 'Center of Rows,Columns/Time', '(CoG)Pixelrow', 'Time')
                plt.xlim(len(self.array3), 0)
                plt.plot(self.array3, 'y', linewidth=2, label='center of Columns')
                plt.plot(self.array2, 'c', linewidth=2, label='center of Rows')
                plt.legend(loc=1, fontsize=15)
            if arr3:
                plt.subplot(223)
                self.setplt(350, 0, 'Brightness/Rows,Cols', 'Brightness', 'Rows,Cols')
                plt.plot(arrayCol, 'y', linewidth=2, label='Col')
                plt.plot(arrayRow, 'c', linewidth=2, label='Row')
                plt.legend(loc=1, fontsize=15)
            if arr4:
                plt.subplot(224)
                self.setplt(2, -2, 'Everything/Time', 'Brightness, Cog, Sum', 'Time')
                plt.xlim(len(array4), 0)
                plt.plot(array1scal, 'r', linewidth=2, label='averg. brightness')
                plt.plot(array2scal, 'c', linewidth=2, label='center of rows')
                plt.plot(array3scal, 'y', linewidth=2, label='center of columns')
                plt.plot(array4scal, 'k', linewidth=2, label='sum')
                plt.legend(loc=1, fontsize=10)
            plt.draw()
            plt.pause(0.001)