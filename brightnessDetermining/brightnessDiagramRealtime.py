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
        avgRowbrightness = rowsum/width
        rowArray.append(round(avgRowbrightness))
    return rowArray

def setarr(arr):
    for x in range(len(arr)-1):
        arr[x] = arr[x+1]
    return arr

def setup():
    avergArr = [100] * 100
    plt.figure(figsize=(11, 4.5), dpi=70)
    plt.style.use('fivethirtyeight')
    return avergArr

def setplt(scaleT, scaleB, title, yLabel, xLabel):
    plt.ylim(top=scaleT)
    plt.ylim(bottom=scaleB)
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)

def trueLoop(array1, image, smoothed, counter, frequency, mode):
    if smoothed != False and smoothed != True: print('\033[1;31m Input error! smoothed must be True or False'), exit(0)
    if mode != 1 and mode != 2 and mode != 3: print('\033[1;31m Input error! Mode must be 1, 2 or 3'), exit(0)
    try:
        array1 = setarr(array1)
    except:
        print('\033[1;31m Sequence error! Setup must happen first')
        exit(0)
    try:
        array2 = getRowArray(image)
    except:
        print('\033[1;31m Input error! Image is no image')
        exit(0)
    array1[len(array1) - 1] = round(cv2.mean(np.array(array2))[0])

    if smoothed:
        array1 = gaussian_filter1d(array1, sigma=1)
        array2 = gaussian_filter1d(array2, sigma=8)
    try:
        if counter%frequency == 0:
            plt.clf()
            if mode == 1 or mode == 3:
                if mode == 3:
                    plt.subplot(121)
                setplt(array1.max()+50, array1.min()-50, 'Brightness/Time', 'Brightness', 'Time')
                plt.plot(array1, 'm', linewidth=2)
            if mode == 2 or mode == 3:
                if mode == 3:
                    plt.subplot(122)
                setplt(array2.max()+50, array2.min()-50, 'Brightness/Row', 'Brightness', 'Pixelrows from image')
                plt.plot(array2, 'c', linewidth=2)
            plt.draw()
    except:
        print('\033[1;31m Division by zero error! Frequency must not be zero')
        exit(0)

    plt.pause(0.0001)
