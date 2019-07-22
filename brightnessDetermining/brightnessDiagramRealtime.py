from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np
import cv2

def resize(img, percent):
    scale_percent = percent  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

def getRowArray(img):
    height, width = img.shape[:2]
    rowArray = []
    for x in range(height):
        rowsum = cv2.sumElems(img[x])[0]
        avgRowbrightness = rowsum/height
        rowArray.append(round(avgRowbrightness))
    return rowArray

def setarr(arr):
    for x in range(len(arr)-1):
        arr[x] = arr[x+1]
    return arr

def setup():
    avergArr = [10] * 200
    plt.figure(figsize=(8, 3), dpi=80)
    return avergArr

def setplt(scaleT, scaleB, title, yLabel, xLabel):
    plt.ylim(top=scaleT)
    plt.ylim(bottom=scaleB)
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)

def trueLoop(array1, image, smoothed, counter, frequency, mode):
    array1 = setarr(array1)
    array2 = getRowArray(image)
    array1[len(array1) - 1] = round(cv2.mean(np.array(array2))[0])

    if smoothed:
        array1 = gaussian_filter1d(array1, sigma=1)
        array2 = gaussian_filter1d(array2, sigma=8)

    if counter%frequency == 0:
        plt.clf()
        if mode == 1 or mode == 3:
            if mode == 3:
                plt.subplot(121)
            setplt(350, 0, 'Average Brightness over time', 'Brightness', 'Time')
            plt.plot(array1)
        if mode == 2 or mode == 3:
            if mode == 3:
                plt.subplot(122)
            setplt(350, 0, 'Overall Brightness, starting from the top', 'Brightness', 'Pixelrows from image')
            plt.plot(array2)
        plt.draw()

    plt.pause(0.0001)
