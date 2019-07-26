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
        for x in range(len(arr)-2, -1, -1):
            arr[x+1] = arr[x]
        return arr
    except:
        print('\033[1;31m Sequence error! Setup must happen first')
        exit(0)

def setup():
    array1 = []
    array3 = []
    plt.ioff()
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

def trueLoop(arrays, sec, image, counter, smoothed = True, scaling = False, frequency = 1, arr1 = True, arr2 = False, arr3 = False, arr4 = True):
    if frequency == 1:
        if sec != 0: fps = round(1.0/sec, 1)
        else: fps = 0
    else:
        fps = None

    array1 = arrays[0]
    array3 = arrays[1]
    array2 = getRowArray(image)

    coG = getCoG(array2)

    if len(array1) < 50:

        array1.insert(0, round(cv2.mean(np.array(array2))[0]))
        array3.insert(0, coG)
    else:
        array1[0] = round(cv2.mean(np.array(array2))[0])
        array3[0] = coG
        array1 = setarr(array1)
        array3 = setarr(array3)

    array4 = np.array([sum(x) for x in zip(*[array1, array3])])


    if counter%frequency == 0:
        if scaling:
            array1 = scaleArr(array1)
            array3 = scaleArr(array3)
            array4 = scaleArr(array4)
            buffer = 2
        else: buffer = 50
        if smoothed:
            array1 = gaussian_filter1d(array1, sigma=1)
            array2 = gaussian_filter1d(array2, sigma=1)
            array3 = gaussian_filter1d(array3, sigma=1)
            array4 = gaussian_filter1d(array4, sigma=1)
        array1 = np.around(array1, decimals=2)
        array2 = np.around(array2, decimals=2)
        array3 = np.around(array3, decimals=2)
        array4 = np.around(array4, decimals=2)

        #print(array1, array3, array4)
        plt.clf()
        plt.suptitle('fps: ' + str(fps), fontsize=16)
        if arr1:
            plt.subplot(221)
            setplt(max(array1)+buffer, min(array1)-buffer, 'Average Brightness/Time', 'Brightness', 'Time')
            plt.xlim(len(array1), 0)
            plt.plot(array1, 'r', linewidth=2, label='averg. brightness')
            plt.legend(loc=1, fontsize=20)
        if arr2:
            plt.subplot(222)
            setplt(max(array3)+buffer, min(array3)-buffer, 'CenterOfGravity/Time', '(CoG)Pixelrow', 'Time')
            plt.xlim(len(array3), 0)
            plt.plot(array3, 'c', linewidth=2, label='center of gravity')
            plt.legend(loc=1, fontsize=20)
        if arr3:
            plt.subplot(223)
            setplt(max(array4)+buffer, min(array4)-buffer, 'Sum/Time', 'Sum', 'Time')
            plt.xlim(len(array4), 0)
            plt.plot(array4, 'k', linewidth=2, label='sum')
            plt.legend(loc=1, fontsize=20)
        if arr4:
            plt.subplot(224)
            #plot(300, 0, 'Brightness/Row', 'Brightness', 'Pixelrow')
            #plt.scatter(coG, 100, s=50)
            #plt.plot(array2, 'k', linewidth=2)

            setplt(2, -2, 'Everything/Time', 'Brightness, Cog, Sum', 'Time')
            plt.xlim(len(array4), 0)
            plt.plot(scaleArr(array1), 'r', linewidth=2, label='averg. brightness')
            plt.plot(scaleArr(array3), 'c', linewidth=2, label='center of gravity')
            plt.plot(scaleArr(array4), 'k', linewidth=2, label='sum')
            plt.legend(loc=1, fontsize=13)

        plt.draw()
        plt.pause(0.001)