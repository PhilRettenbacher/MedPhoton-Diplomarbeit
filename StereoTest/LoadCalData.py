from stereovision import calibration
from ImagingApi import ImagingApi
from stereovision.ui_utils import BMTuner
from stereovision.blockmatchers import StereoSGBM
import os
import cv2

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")

cam = ImagingApi.CameraApi(False, (1,0))
left_image, right_image = cam.getPicture()

left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

block_matcher = cv2.StereoBM_create()

rectified_pair = calib_loaded.rectify((left_image, right_image))

cv2.imshow("1",rectified_pair[0])
cv2.imshow("2",rectified_pair[1])

block_matcher = StereoSGBM()

tuner = BMTuner(block_matcher, calib_loaded, rectified_pair)

cv2.waitKey(1)

