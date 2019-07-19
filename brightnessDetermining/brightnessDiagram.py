import cv2
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

image = 'testpic.jpg'
img_rgb = cv2.imread(image)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

def resize(img):
    scale_percent = 50  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

img_gray = resize(img_gray)

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

def calcAvergBrightness(arr):
    sum = 0
    for x in range(len(arr)):
        sum += arr[x]
    averg = round(sum/len(arr))
    newarr = []
    for x in range(len(arr)):
        newarr.append(averg)
    return newarr

img_gray = resize(img_gray)
cv2.imshow("image", img_gray)

yArr = getRowArray(img_gray)
ysmoothed = gaussian_filter1d(yArr, sigma=20)

plt.plot(yArr)                          #original curve
plt.plot(ysmoothed)                     #smoothed curve
plt.plot(calcAvergBrightness(yArr))     #average brightness of curve

plt.xlabel("Pixelrow")
plt.ylabel("Brightness")
plt.show()