import cv2
from Calibration import StereoCalibration
from Calibration import MonoCalibration
import numpy
from brightnessDetermining import brightnessDiagramRealtime as bdr
from ImagingApi import ImagingApi

imLeft = cv2.imread("CalibL/imageFrame_0_0.jpg")
imRight = cv2.imread("CalibR/imageFrame_1_0.jpg")

calibL = MonoCalibration.MonoCalibrator((8, 6), imLeft.shape[0:2])
calibR = MonoCalibration.MonoCalibrator((8, 6), imLeft.shape[0:2])

recalibrate = False

calDataL = None
calDataR = None

if(recalibrate):

    lCount = 67
    rCount = 60

    for x in range(0, lCount):
        img = cv2.imread("CalibL/imageFrame_0_"+str(x)+".jpg")
        calibL.addCheckerBoard(img)
    for x in range(0, rCount):
        img = cv2.imread("CalibR/imageFrame_1_"+str(x)+".jpg")
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

#cv2.imshow("undistL", calib.undistort(imLeft, True))
#cv2.imshow("distL", imLeft)

#cv2.imshow("a",imLeft)
#cv2.imshow("n", cv2.undistort(imLeft, calDataL[1], calDataL[2]))
#cv2.waitKey(0)

dualCalCount = 47

for x in range(0, dualCalCount):
    imLeft = cv2.imread("DualCalib/imageFrame_0_"+str(x)+".jpg")
    imRight = cv2.imread("DualCalib/imageFrame_1_"+str(x)+".jpg")
    ret = calib.addCheckerBoard(imLeft, imRight, False, False, 0)
    print(ret[0] and ret[1])


calib.calibrate(shearing=True)

#cv2.imshow("rectify", calib.re1ctifyImg(calib.undistort(imLeft, True), True))
#cv2.imshow("rechtify2", calib.rectifyImg(calib.undistort(imRight, False), False))
#cv2.waitKey(0)

cap = ImagingApi.CameraApi(1024, 768)
cap.keyListener()

minDisp = -16*15
maxDisp = 16*5
bm = cv2.StereoSGBM_create(minDisparity= minDisp, numDisparities=maxDisp-minDisp, blockSize=11, P2=5000, P1=100, uniquenessRatio=0, speckleWindowSize=500, speckleRange=16, disp12MaxDiff=64, preFilterCap=0, mode=cv2.STEREO_SGBM_MODE_HH4)
avergArr = bdr.setup()
counter = 0
while True:
    imLeft, imRight = cap.getFrames()
    imLeft = bdr.resize(imLeft, 50)
    imRight = bdr.resize(imRight, 50)

    iml = calib.rectifyImg(calib.undistort(imLeft, True), True)
    imr = calib.rectifyImg(calib.undistort(imRight, False), False)

    cv2.imshow("L", iml)
    cv2.imshow("R", imr)

    disp = bm.compute(iml, imr)
    disp = (disp - (minDisp - 1) * 16) / (((maxDisp - minDisp)) * 16)

    # Graphics

    bdr.trueLoop(avergArr, disp*800, True, counter, 1, True, True, False, True)

    counter += 1

    cv2.imshow("disp", disp)
    cv2.waitKey(1)

# calib.rectifyImg:	~0.07 sec
# bm.compute:		~0.28 sec
# trueloop:		    ~0.05 sec (jedes xte mal 0.11 sec)
