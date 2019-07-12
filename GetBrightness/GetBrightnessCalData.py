import cv2;
from PIL import Image
import StereoTest
import glob

webcamID = 2
cap = cv2.VideoCapture('http://192.168.199.3:808' + str(webcamID) + '/')
alpha = 3
beta = -150

image = 'DisparityMap.jpg'

def getBrightness(str, x, y):
    imag = Image.open(str)
    imag = imag.convert('RGB')
    pixelRGB = imag.getpixel((x, y))
    R, G, B = pixelRGB
    brightness = sum([R, G, B]) / 3
    return brightness

def printBrightness(event,x,y,flags,param):
    TWHITE = '\033[37m'
    TGREEN = '\033[32m'
    brightness = getBrightness(image, x, y)
    black = 4000 #cm
    white = 10 #cm
    length = 4000/brightness+10
    print(TWHITE + str(brightness) + TGREEN + " = " + str(round(length)) + "cm")

while(True):
    cv2.setMouseCallback(image, printBrightness)
    img = cv2.imread(image, 0)
    cv2.imshow(image, img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()