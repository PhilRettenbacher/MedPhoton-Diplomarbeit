import cv2
from Calibration import StereoCalibration
from Calibration import MonoCalibration
import numpy

imLeft = cv2.imread("CalibL/imageFrame_0_0.jpg")
imRight = cv2.imread("CalibR/imageFrame_0_0.jpg")

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
        img = cv2.imread("CalibR/imageFrame_0_"+str(x)+".jpg")
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

cv2.imshow("undistL", calib.undistort(imLeft, True))
cv2.imshow("distL", imLeft)


for x in range(0, 7):
    imLeft = cv2.imread("DualCalib/imageFrame_0_"+str(x)+".jpg")
    imRight = cv2.imread("DualCalib/imageFrame_1_"+str(x)+".jpg")
    calib.addCheckerBoard(imLeft, imRight, False, True, 0)


cv2.waitKey(0)

calib.calibrate(shearing=True)
cv2.imshow("rectify", calib.rectifyImg(calib.undistort(imLeft, True), True))
cv2.imshow("rechtify2", calib.rectifyImg(calib.undistort(imRight, False), False))
cv2.waitKey(0)