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

    try:
        height, width = img.shape[:2]
        rowArray = []
        for x in range(height):
            rowsum = cv2.sumElems(img[x])[0]
            avgRowbrightness = rowsum/(cv2.countNonZero(img[x])+1)
            rowArray.append(round(avgRowbrightness))
        return rowArray
    except:
        print('\033[1;31m Input error! No image found')
        exit(0)


def setarr(arr):
    try:
        for x in range(len(arr) - 1, -1, -1):
            arr[x] = arr[x - 1]
        return arr
    except:
        print('\033[1;31m Sequence error! Setup must happen first')
        exit(0)

def setup():
    length = 80
    array1 = [450] * length
    array3 = [260] * length
    plt.ion()
    #plt.figure(figsize=(16, 4.5), dpi=70)
    plt.figure(figsize=(15, 12), dpi=60)
    plt.style.use('fivethirtyeight')
    return array1, array3

def plot(arr, timeAx, title, yLabel, xLabel, color):
    buffer = 10
    if timeAx: plt.xlim(len(arr), 0)
    plt.ylim(top=max(arr)+buffer)
    plt.ylim(bottom=min(arr)-buffer)
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.plot(arr, color, linewidth=2)

def getCoG(arr):
    sum = cv2.sumElems(np.array(arr))[0]
    i = 0
    for x in range(len(arr)):
        i+=arr[x]
        if i >= (sum/2):
            return x

def trueLoop(arrays, image, smoothed, counter, frequency, arr1, arr2, arr3, arr4):

    array1 = setarr(arrays[0])
    array3 = setarr(arrays[1])
    array2 = getRowArray(image)
    array4 = np.array([sum(x) for x in zip(*[array1, array3])])

    coG = getCoG(array2)
    array3[0] = coG
    array1[0] = round(cv2.mean(np.array(array2))[0])

    if smoothed:
        array1 = gaussian_filter1d(array1, sigma=2)
        array2 = gaussian_filter1d(array2, sigma=8)
        array3 = gaussian_filter1d(array3, sigma=3)
        array4 = gaussian_filter1d(array4, sigma=3)

    if counter%frequency == 0:
        plt.clf()

        if arr1:
            plt.subplot(221)
            plot(array1, True, 'Average Brightness/Time', 'Brightness', 'Time', 'r')
        if arr2:
            plt.subplot(222)
            plot(array3, True, 'CenterOfGravity/Time', '(CoG)Pixelrow', 'Time', 'm')
        if arr3:
            plt.subplot(223)
            plot(array2, False, 'Brightness/Row', 'Brightness', 'Pixelrow', 'c')
            plt.scatter(coG, array1[0], s=50)
        if arr4:
            plt.subplot(224)
            plot(array4, True, 'Sum/Time', 'Sum', 'Time', 'b')


        plt.draw()
        plt.pause(0.001)

