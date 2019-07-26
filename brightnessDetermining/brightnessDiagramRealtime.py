from scipy.ndimage.filters import gaussian_filter1d
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cv2

class brightnessDiagramRealtime:
    def __init__(self):
        self.oldtime=0
        self.array1 = np.array([])
        self.array2 = np.array([])
        self.array3 = np.array([])
        plt.ioff()
        plt.figure("YourWindowName", figsize=(15, 10), dpi=50)
        plt.style.use('fivethirtyeight')

    def resize(self, img, percent):
        scale_percent = percent  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    def getRowArray(self, img):
        try:
            height, width = img.shape[:2]
            rowArray = []
            for x in range(height):
                rowsum = cv2.sumElems(img[x])[0]
                avgRowbrightness = rowsum/cv2.countNonZero(img[x])
                rowArray.append(round(avgRowbrightness))
            return rowArray
        except:
            print('\033[1;31m Input error! No image found')
            exit(0)

    def getColArray(self, img):
        try:
            height, width = img.shape[:2]
            colArray = []
            for x in range(height):
                colsum = cv2.sumElems(img[:,x])[0]
                avgColbrightness = colsum/cv2.countNonZero(img[x])
                colArray.append(round(avgColbrightness))
            return colArray
        except:
            print('\033[1;31m Input error! No image found')
            exit(0)

    def setarr(self, arr):
        try:
            for x in range(len(arr)-2, -1, -1):
                arr[x+1] = arr[x]
            return arr
        except:
            print('\033[1;31m Sequence error! Setup must happen first')
            exit(0)

    def setplt(self, scaleT, scaleB, title, yLabel, xLabel):
        plt.ylim(top=scaleT)
        plt.ylim(bottom=scaleB)
        plt.title(title)
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)

    def getComR(self, arr):
        sum = cv2.sumElems(np.array(arr))[0]
        i = 0
        for x in range(len(arr)):
            i+=arr[x]
            if i >= (sum/2):
                return x

    def getComC(self, arr):
        sum = cv2.sumElems(np.array(arr))[0]
        i = 0
        for x in range(len(arr)):
            i+=arr[x]
            if i >= (sum/2):
                return x

    def scaleArr(self, arr):
        arr = np.interp(arr, (arr.min(), arr.max()), (-1, +1))
        return arr

    def trueLoop(self, image, counter, smoothed = True, scaling = False, frequency = 1, arr1 = True, arr2 = True, arr3 = True, arr4 = True):

        sec = float(datetime.datetime.now().strftime('%S.%f')) - self.oldtime
        self.oldtime = float(datetime.datetime.now().strftime('%S.%f'))
        if frequency == 1:
            if sec != 0: fps = round(1.0/sec, 1)
            else: fps = 0
        else:
            fps = None

        arrayRow = self.getRowArray(image)
        arrayCol = self.getColArray(image)

        comR = self.getComR(arrayRow)
        comC = self.getComC(arrayCol)
        if len(self.array1) < 50:
            self.array1 = np.insert(self.array1, 0, round(cv2.mean(np.array(arrayRow))[0]))
            self.array2 = np.insert(self.array2, 0, comR)
            self.array3 = np.insert(self.array3, 0, comC)
        else:
            self.array1[0] = round(cv2.mean(np.array(arrayRow))[0])
            self.array2[0] = comR
            self.array3[0] = comC
            self.array1 = self.setarr(self.array1)
            self.array2 = self.setarr(self.array2)
            self.array3 = self.setarr(self.array3)

        array4 = np.array([sum(x) for x in zip(*[self.array1, self.array2, self.array3])])

        if counter%frequency == 0:
            if scaling:
                self.array1 = self.scaleArr(self.array1)
                self.array2 = self.scaleArr(self.array2)
                self.array3 = self.scaleArr(self.array3)
                array4 = self.scaleArr(array4)
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

            print(self.array1, self.array3, self.array2)
            plt.clf()
            plt.suptitle('fps: ' + str(fps), fontsize=16)
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
                self.setplt(350, 0, 'Rows,Cols/Time', 'Rows,Cols', 'Time')
                plt.plot(arrayCol, 'y', linewidth=2, label='Col')
                plt.plot(arrayRow, 'c', linewidth=2, label='Row')
                plt.legend(loc=1, fontsize=15)
            if arr4:
                plt.subplot(224)
                self.setplt(2, -2, 'Everything/Time', 'Brightness, Cog, Sum', 'Time')
                plt.xlim(len(array4), 0)
                plt.plot(self.scaleArr(self.array1), 'r', linewidth=2, label='averg. brightness')
                plt.plot(self.scaleArr(self.array2), 'c', linewidth=2, label='center of rows')
                plt.plot(self.scaleArr(self.array3), 'y', linewidth=2, label='center of columns')
                plt.plot(self.scaleArr(array4), 'k', linewidth=2, label='sum')
                plt.legend(loc=1, fontsize=10)
            plt.draw()
            plt.pause(0.001)

