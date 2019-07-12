import cv2;
from PIL import Image

webcamID = 2
cap = cv2.VideoCapture('http://192.168.199.3:808' + str(webcamID) + '/')
alpha = 3
beta = -150

live = True

def getBrightness(str, x, y):
    imag = Image.open(str)
    imag = imag.convert('RGB')
    pixelRGB = imag.getpixel((x, y))
    R, G, B = pixelRGB
    brightness = sum([R, G, B]) / 3
    return brightness

def printBrightness(event,x,y,flags,param):
    TWHITE = '\033[37m'
    print(TWHITE + str(getBrightness("image.jpg", x, y)))

if live == False:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.convertScaleAbs(frame, frame, alpha, beta);
    cv2.imwrite("image.jpg", frame)
    cv2.namedWindow('image')

while(True):
    # Cam connection
    if live:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.convertScaleAbs(frame, frame, alpha, beta);
        cv2.imwrite("image.jpg", frame)
        cv2.namedWindow('image')

    cv2.setMouseCallback('image', printBrightness)
    cv2.imshow('image', frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()