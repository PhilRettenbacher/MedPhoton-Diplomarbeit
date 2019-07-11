from stereovision import calibration
from ImagingApi import ImagingApi
import keyboard
import os
import cv2

cam = ImagingApi.CameraApi(False, (1,2))

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")

mindisparity = -21
numdisparites = 96
blocksize = 21

specklerange = 8
specklewindowsize = 0
preFilterSize = 13
smallerBlockSize = 1
textureThreshold = 0

while True:
    left_image, right_image = cam.getPicture()

    left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    rectified_pair = calib_loaded.rectify((left_image, right_image))

    cv2.imshow("1",rectified_pair[0])
    cv2.imshow("2",rectified_pair[1])

    block_matcher = cv2.StereoSGBM_create()

    block_matcher.setMinDisparity(mindisparity)
    block_matcher.setNumDisparities(numdisparites)
    block_matcher.setBlockSize(blocksize)
    block_matcher.setSpeckleRange(specklerange)
    block_matcher.setSpeckleWindowSize(specklewindowsize)
    block_matcher.setPreFilterCap(preFilterSize)
    block_matcher.setUniquenessRatio(2)
    block_matcher.setDisp12MaxDiff(15)
    block_matcher.setP1(1000)
    block_matcher.setP2(1000)
    #block_matcher.setSmallerBlockSize(smallerBlockSize)
    #block_matcher.setTextureThreshold(textureThreshold)

    disparity = block_matcher.compute(rectified_pair[0],rectified_pair[1])
    cv2.imshow('Ja', cv2.normalize(disparity, alpha=0, beta=255, dst=None, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U))
    cv2.waitKey(1)

    if keyboard.is_pressed('1'):
        mindisparity += 1
        print ("mindisparity: " + str(mindisparity))
    if keyboard.is_pressed('2'):
        mindisparity -= 1
        print ("mindisparity: " + str(mindisparity))

    if keyboard.is_pressed('3'):
        numdisparites += 16
        print ("numdisparites: " + str(numdisparites))
    if keyboard.is_pressed('4'):
        numdisparites -= 16
        print ("numdisparites: " + str(numdisparites))

    if keyboard.is_pressed('5'):
        blocksize += 1
        print ("blocksize: " + str(blocksize))
    if keyboard.is_pressed('6'):
        blocksize -= 1
        print ("blocksize: " + str(blocksize))

    if keyboard.is_pressed('7'):
        specklerange += 1
        print ("specklerange: " + str(specklerange))
    if keyboard.is_pressed('8'):
        specklerange -= 1
        print ("specklerange: " + str(specklerange))

    if keyboard.is_pressed('9'):
        specklewindowsize += 1
        print ("specklewindowsize: " + str(specklewindowsize))
    if keyboard.is_pressed('0'):
        specklewindowsize -= 1
        print ("specklewindowsize: " + str(specklewindowsize))


#disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

#cv2.imshow("StereoCam", disparity / 255.)

#cv2.waitKey(0)