from stereovision import calibration
from ImagingApi import ImagingApi
import os
import cv2

cam = ImagingApi.CameraApi(False, (1,2))

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")

mindisparity = 2
numdisparites = 80
blocksize = 15
specklerange = 1
specklewindowsize = 12
preFilterSize = 0
smallerBlockSize = 10
textureThreshold = 1

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
    #block_matcher.setSmallerBlockSize(smallerBlockSize)
    #block_matcher.setTextureThreshold(textureThreshold)

    disparity = block_matcher.compute(rectified_pair[0],rectified_pair[1])
    cv2.imshow('Ja', disparity / 1024.)
    cv2.waitKey(1)

    if cv2.waitKey(10) == 32:
        preFilterSize+=10

    print(preFilterSize)

#disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

#cv2.imshow("StereoCam", disparity / 255.)

#cv2.waitKey(0)