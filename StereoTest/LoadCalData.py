from stereovision import calibration
from ImagingApi import ImagingApi
import keyboard
import os
import cv2

cam = ImagingApi.CameraApi(True, (1,2))

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")
mindisparity = 2
numdisparites = 64
blocksize = 15
specklerange = 12
specklewindowsize = 2
mode = "mindisparity"

while True:
    left_image, right_image = cam.getPicture()

    left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    rectified_pair = calib_loaded.rectify((left_image, right_image))

    cv2.imshow("1",rectified_pair[0])
    cv2.imshow("2",rectified_pair[1])

    block_matcher = cv2.StereoBM_create(numDisparities=16, blockSize=15)


    block_matcher.setMinDisparity(mindisparity)
    block_matcher.setNumDisparities(numdisparites)
    block_matcher.setBlockSize(blocksize)
    block_matcher.setSpeckleRange(specklerange)
    block_matcher.setSpeckleWindowSize(specklewindowsize)

    disparity = block_matcher.compute(rectified_pair[0],rectified_pair[1])
    cv2.imshow('Ja', disparity / 1024.)
    cv2.waitKey(1)

    def format_coord(x, y):
        return "text_string_made_from({:.2f},{:.2f})".format(x, y)
    cv2.format_coord = format_coord

    if keyboard.is_pressed('1'):
        mindisparity += 1
        print ("mindisparity: " + str(mindisparity))
    if keyboard.is_pressed('2'):
        mindisparity -= 1
        print ("mindisparity: " + str(mindisparity))

    if keyboard.is_pressed('3'):
        numdisparites += 1
        print ("numdisparites: " + str(numdisparites))
    if keyboard.is_pressed('4'):
        numdisparites -= 1
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