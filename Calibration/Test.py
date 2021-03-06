import cv2
from Calibration import StereoCalibration
from Calibration import MonoCalibration
import numpy
import datetime
from brightnessDetermining import breathingDiagram
from ImagingApi import ImagingApi

imLeft = cv2.imread("CalibL/imageFrame_0_0.jpg")
imRight = cv2.imread("CalibR/imageFrame_1_0.jpg")

calibL = MonoCalibration.MonoCalibrator((8, 6), imLeft.shape[0:2])
calibR = MonoCalibration.MonoCalibrator((8, 6), imLeft.shape[0:2])

recalibrate = False
calDataL = None
calDataR = None

#calculate the intrinsic and distortion parameters
if(recalibrate):

    lCount = 24
    rCount = 74

    for x in range(0, lCount):
        img = cv2.imread("calibLTest/imageFrame_0_"+str(x)+".jpg")
        print(x)
        calibL.addCheckerBoard(img)
    for x in range(0, rCount):
        img = cv2.imread("calibRTest/imageFrame_0_"+str(x)+".jpg")
        calibR.addCheckerBoard(img)

    print("calibrating...")
    calibL.calibrateCamera()
    print("left Camera calibration finished")
    calDataL = calibL.getCalibData()
    numpy.save("LeftCalib.npy", calDataL)

    calibR.calibrateCamera()
    print("calibration finished")
    calDataR = calibR.getCalibData()
    numpy.save("RightCalib.npy", calDataR)

    cv2.waitKey(0)

else:
    calDataL = numpy.load("LeftCalib.npy", allow_pickle=True)
    calDataR = numpy.load("RightCalib.npy", allow_pickle=True)

calib = StereoCalibration.StereoCalibrator((8, 6), imLeft.shape[0:2], calDataL, calDataR)
print("Delta: " + str(calDataL[2]-calDataR[2]))

imLeft = cv2.imread("CalibLTest/imageFrame_0_0.jpg")
imRight = cv2.imread("CalibRTest/imageFrame_0_0.jpg")

cv2.imshow("l", calib.undistort(imLeft, True))
cv2.imshow("r", calib.undistort(imRight, False))

dualCalCount = 13
dualCalStart = 0

#calculate the rectification maps
for x in range(dualCalStart, dualCalCount):
    imLeft = cv2.imread("DualCalibTest/imageFrame_0_"+str(x)+".jpg")
    imRight = cv2.imread("DualCalibTest/imageFrame_1_"+str(x)+".jpg")
    ret = calib.addCheckerBoard(imLeft, imRight, False, False, 0)
    print(ret[0] and ret[1])


calib.calibrate(shearing=True)

imLeft = cv2.imread("DualCalibTest/imageFrame_0_0.jpg")
imRight = cv2.imread("DualCalibTest/imageFrame_1_0.jpg")
iml = calib.rectifyImg(calib.undistort(imLeft, True), True)
imr = calib.rectifyImg(calib.undistort(imRight, False), False)


cv2.imshow("L", iml)
cv2.imshow("R", imr)
cv2.waitKey(0)

cap = ImagingApi.CameraApi(640, 480, useWeb=False)
cap.keyListener()


minDisp = -16*10
maxDisp = 16*10
bm = cv2.StereoSGBM_create(minDisparity= minDisp, numDisparities=maxDisp-minDisp, blockSize=11, P2=4000, P1=1500, uniquenessRatio=4, speckleWindowSize=100, speckleRange=16, disp12MaxDiff=64, preFilterCap=5)

counter = 7
sec = 0

bdr = breathingDiagram.BreathingPlotter((breathingDiagram.BreathPlot.WEIGHT_COL_TIME,
                                            breathingDiagram.BreathPlot.WEIGHT_ROW_TIME,
                                            breathingDiagram.BreathPlot.AVG_BRIGHT_TIME,
                                            breathingDiagram.BreathPlot.SUM_TIME), imLeft.shape, smooth=True, frequency=1, autoscale=True)
while True:
    imLeft, imRight = cap.getFrames()

    #tmpCap1 = (cv2.VideoCapture(
    #    "http://192.168.199.3:8765/picture/1/current/?_username=admin&_signature=405e3e47c0b54c48c7539decf8437b48bb320e16"))
    #found1, imLeft = tmpCap1.read()
    #tmpCap2 = (cv2.VideoCapture(
    #    "http://192.168.199.3:8765/picture/2/current/?_username=admin&_signature=8364b7955ab9bcfe1b2717c91ea1b2d6f2f59a6a"))
    #found2, imRight = tmpCap2.read()

    #rectify images
    iml = calib.rectifyImg(calib.undistort(imLeft, True), True)
    imr = calib.rectifyImg(calib.undistort(imRight, False), False)

    cv2.imshow("L", iml)
    cv2.imshow("R", imr)

    disp = bm.compute(iml, imr)

    disp = (disp - (minDisp - 1) * 16) / (((maxDisp - minDisp)) * 16)

    #disp = disp.astype('float32')

    #disp = cv2.cvtColor(disp, cv2.COLOR_GRAY2RGB)
    #cv2.imshow("overlay", iml.astype("float32")*0.002+disp*0.7)
    # Graphics

    #bdr.trueLoop(counter, disp*1000, frequency=1, scaling=False, arr1=True, arr2=True, arr3=True)
    counter += 1

    cv2.imshow("disp", disp)
    cv2.waitKey(1)
    b = datetime.datetime.now().strftime('%S.%f')
    sec = float(b) - float(a)
    bdr.update(disp * 255)

# calib.rectifyImg:	~0.07 sec
# bm.compute:		~0.28 sec
# trueloop:		    ~0.05 sec (jedes xte mal 0.11 sec)
