import cv2
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

def resize(img):
    scale_percent = 100  # percent of original size
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

def setup():
    avergArr = [10] * 200
    plt.figure(figsize=(8, 3), dpi=80)
    return avergArr

def trueLoop(avergArr, image):
    # Overall Brightness
    img_gray = image#cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray = resize(img_gray)
    yArr = getRowArray(img_gray)
    ysmoothed = gaussian_filter1d(yArr, sigma=4)

    plt.subplot(1, 2, 2)
    plt.ylim(top=350)
    plt.ylim(bottom=0)
    plt.title('Overall Brightness, starting from the top')
    plt.ylabel("Brightness")
    plt.xlabel('Pixelrows from image')
    #plt.plot(yArr)
    plt.plot(ysmoothed)
    # plt.plot(calcAvergBrightnessArr(yArr))

    # Realtime Average
    avergArr = setarr(avergArr)
    avergsmoothed = gaussian_filter1d(avergArr, sigma=1)
    avergArr[len(avergArr) - 1] = calcAvergBrightness(yArr)

    plt.subplot(1, 2, 1)
    plt.ylim(top=350)
    plt.ylim(bottom=0)
    plt.title('Average Brightness over time')
    plt.ylabel('brightness')
    plt.xlabel('Time')
    #plt.plot(avergArr)
    plt.plot(avergsmoothed)

    plt.draw()
    plt.pause(0.001)
    plt.clf()

    #cv2.imshow("image", img_gray)
