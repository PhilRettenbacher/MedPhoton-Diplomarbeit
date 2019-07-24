from scipy.ndimage.filters import gaussian_filter1d
import matplotlib
matplotlib.use('TkAgg')
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
    length = 100
    array1 = []
    array3 = []
    plt.ion()
    plt.figure("YourWindowName", figsize=(15, 12), dpi=60)
    plt.style.use('fivethirtyeight')
    return array1, array3

def setplt(scaleT, scaleB, title, yLabel, xLabel):
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

def scaleArr(arr):
    #print(arr)
    arr = np.interp(arr, (np.array(arr).min(), np.array(arr).max()), (-1, +1))
    return arr

def trueLoop(arrays,sec, image, smoothed, counter, frequency, arr1, arr2, arr3, arr4):
    if sec != 0: fps = round(1.0/sec, 1)
    else: fps = 0

    array1 = arrays[0]
    array3 = arrays[1]
    array2 = getRowArray(image)

    #array2 = [i - round(cv2.mean(np.array(array2))[0]) for i in array2]

    coG = getCoG(array2)
    if len(array1) <= 100:
        array1.insert(0, round(cv2.mean(np.array(array2))[0]))
        array3.insert(0, coG)
    else:
        array1[0] = round(cv2.mean(np.array(array2))[0])
        array3[0] = coG
        array1 = setarr(array1)
        array3 = setarr(array3)

    array1 = scaleArr(array1)
    array3 = scaleArr(array3)
    array4 = np.array([sum(x) for x in zip(*[array1, array3])])
    array4 = scaleArr(array4)

    if smoothed:
        array1 = gaussian_filter1d(array1, sigma=2)
        array2 = gaussian_filter1d(array2, sigma=8)
        array3 = gaussian_filter1d(array3, sigma=3)
        array4 = gaussian_filter1d(array4, sigma=3)

    if counter%frequency == 0:
        plt.clf()
        buffer = 2
        plt.suptitle('fps: ' + str(fps), fontsize=16)
        if arr1:
            plt.subplot(221)
            setplt(buffer, -buffer, 'Average Brightness/Time', 'Brightness', 'Time')
            plt.xlim(len(array1), 0)
            plt.plot(array1, 'r', linewidth=2, label='averg. brightness')
            plt.legend(loc=1, fontsize=20)
        if arr2:
            plt.subplot(222)
            setplt(buffer, -buffer, 'CenterOfGravity/Time', '(CoG)Pixelrow', 'Time')
            plt.xlim(len(array3), 0)
            plt.plot(array3, 'c', linewidth=2, label='center of gravity')
            plt.legend(loc=1, fontsize=20)
        if arr3:
            plt.subplot(223)
            setplt(buffer, -buffer, 'Sum/Time', 'Sum', 'Time')
            plt.xlim(len(array4), 0)
            plt.plot(array4, 'k', linewidth=2, label='sum')
            plt.legend(loc=1, fontsize=20)
        if arr4:
            plt.subplot(224)
            #plot(300, 0, 'Brightness/Row', 'Brightness', 'Pixelrow')
            #plt.scatter(coG, 100, s=50)
            #plt.plot(array2, 'k', linewidth=2)

            setplt(buffer, -buffer, 'Everything/Time', 'Brightness, Cog, Sum', 'Time')
            plt.xlim(len(array4), 0)
            plt.plot(array1, 'r', linewidth=2, label='averg. brightness')
            plt.plot(array3, 'c', linewidth=2, label='center of gravity')
            plt.plot(array4, 'k', linewidth=2, label='sum')
            plt.legend(loc=1, fontsize=13)

        plt.draw()
        plt.pause(0.001)