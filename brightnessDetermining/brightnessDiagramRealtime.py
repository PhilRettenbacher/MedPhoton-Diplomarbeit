import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

def read(cap):
    ret, image = cap.read()
    return image

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

def resize(img):
    scale_percent = 50  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

def getRowArray(img):
    width, height = img.shape[:2]
    rowArray = []
    for x in range(width):
        rowsum = 0
        for y in range(height):
            brightness = img[x][y]
            rowsum += brightness
        avgRowbrightness = rowsum/width
        rowArray.append(round(avgRowbrightness))
    return rowArray

def calcAvergBrightnessArr(arr):
    sum = 0
    for x in range(len(arr)):
        sum += arr[x]
    averg = round(sum/len(arr))
    newarr = []
    for x in range(len(arr)):
        newarr.append(averg)
    return newarr

def calcAvergBrightness(arr):
    sum = 0
    for x in range(len(arr)):
        sum += arr[x]
    averg = round(sum/len(arr))
    return averg

def setarr(arr):
    for x in range(len(arr)-1):
        arr[x] = arr[x+1]
    return arr

avergArr = [10] * 200

smoothness = 20
while True:
    img_gray = cv2.cvtColor(read(cap), cv2.COLOR_BGR2GRAY)
    img_gray = resize(img_gray)
    cv2.imshow("image", img_gray)

    yArr = getRowArray(img_gray)
    ysmoothed = gaussian_filter1d(yArr, sigma=smoothness)

    avergArr = setarr(avergArr)
    avergsmoothed = gaussian_filter1d(avergArr, sigma=5)

    plt.plot(avergArr)
    plt.plot(avergsmoothed)


    #plt.plot(yArr)
    #plt.plot(ysmoothed)
    #plt.plot(calcAvergBrightnessArr(yArr))
    avergArr[len(avergArr) - 1] = calcAvergBrightness(yArr)

    plt.ylabel("Brightness")
    plt.title('graph')
    plt.ylim(top=400)
    plt.ylim(bottom=0)
    plt.draw()
    plt.pause(0.000000001)
    plt.clf()