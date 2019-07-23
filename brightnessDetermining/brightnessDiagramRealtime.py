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
            avgRowbrightness = rowsum/cv2.countNonZero(img[x])
            rowArray.append(round(avgRowbrightness))
        return rowArray
    except:
        print('\033[1;31m Input error! Image is no image')
        exit(0)

def setarr(arr):
    try:
        for x in range(len(arr)-1):
            arr[x] = arr[x+1]
        return arr
    except:
        print('\033[1;31m Sequence error! Setup must happen first')
        exit(0)

def setup():
    array1 = [0] * 100
    array3 = [0] * 100
    plt.figure(figsize=(16, 4.5), dpi=70)
    plt.style.use('fivethirtyeight')
    return array1, array3

def setplt(position, scaleT, scaleB, title, yLabel, xLabel):
    plt.subplot(position)
    plt.ylim(top=scaleT)
    plt.ylim(bottom=scaleB)
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)

def getCoG(arr):
    sum = cv2.sumElems(np.array(arr))[0]
    i = 0
    for x in range(len(arr)):
        i+=arr[x]
        if i >= (sum/2):
            return x

def trueLoop(arrays, image, smoothed, counter, frequency, mode=3):

    array1 = setarr(arrays[0])
    array3 = setarr(arrays[1])
    array2 = getRowArray(image)

    coG = getCoG(array2)
    array1[len(array1) - 1] = round(cv2.mean(np.array(array2))[0])
    array3[len(array3) - 1] = coG

    if smoothed:
        array1 = gaussian_filter1d(array1, sigma=1)
        array2 = gaussian_filter1d(array2, sigma=8)
        array3 = gaussian_filter1d(array3, sigma=1)

    if counter%frequency == 0:
        plt.clf()

        # Plot1
        setplt(131, array1.max()+50, array1.min()-50, 'Average Brightness/Time', 'Brightness', 'Time')
        plt.plot(array1, 'r', linewidth=2)

        # Plot2
        setplt(132, array3.max()+50, array3.min()-50, 'CenterOfGravity/Time', '(CoG)Pixelrow', 'Time')
        plt.plot(array3, 'm', linewidth=2)

        # Plot3
        setplt(133, 300, 0, 'Brightness/Row', 'Brightness', 'Pixelrow')
        plt.scatter(coG, 100, s=50)
        plt.plot(array2, 'c', linewidth=2)

        plt.draw()

    plt.pause(0.0001)
