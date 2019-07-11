from stereovision import calibration
from ImagingApi import ImagingApi
from stereovision.ui_utils import BMTuner
from stereovision.blockmatchers import StereoSGBM
import os
import cv2

cam = ImagingApi.CameraApi(False, (1,2))

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")



left_image, right_image = cam.getPicture()

left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

rectified_pair = calib_loaded.rectify((left_image, right_image))

cv2.imshow("1",rectified_pair[0])
cv2.imshow("2",rectified_pair[1])

block_matcher = StereoSGBM()

tuner = BMTuner(block_matcher, calib_loaded, rectified_pair)

#disparity = block_matcher.compute(rectified_pair[0],rectified_pair[1])
#cv2.imshow('Ja', disparity / 1024.)
cv2.waitKey(1)


#disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

#cv2.imshow("StereoCam", disparity / 255.)

#cv2.waitKey(0)