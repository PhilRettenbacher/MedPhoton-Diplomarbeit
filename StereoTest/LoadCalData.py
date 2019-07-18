from stereovision import calibration
from ImagingApi import ImagingApi
from sklearn.preprocessing import normalize
from stereovision.ui_utils import BMTuner
from stereovision.blockmatchers import StereoSGBM
import os
import cv2
import numpy as np

calib_loaded = calibration.StereoCalibration(input_folder=os.getcwd()+"/CalData")

cam = ImagingApi.CameraApi(False, (1, 0))
live = False
def getDisparity():
    left_image, right_image = cam.getPicture()

    #left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    #right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    block_matcher = cv2.StereoBM_create()

    rectified_pair = calib_loaded.rectify((left_image, right_image))
    '''
    cv2.imshow("1",rectified_pair[0])
    cv2.imshow("2",rectified_pair[1])

    block_matcher = StereoSGBM()

    tuner = BMTuner(block_matcher, calib_loaded, rectified_pair)
    '''
    # SGBM Parameters -----------------
    window_size = 3  # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=160,  # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=5,
        P1=8 * 3 * window_size ** 2,
        # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    print('computing disparity...')

    displ = left_matcher.compute(left_image, right_image)  # .astype(np.float32)/16
    dispr = right_matcher.compute(right_image, left_image)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, left_image, None, dispr)  # important to put "imgL" here!!!

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    cv2.imshow('Disparity Map', filteredImg)
    cv2.imshow("1", rectified_pair[0])
    cv2.imshow("2", rectified_pair[1])
    cv2.imwrite('DisparityMap.jpg', filteredImg)

if live:
    while (True):
        getDisparity()
        if cv2.waitKey(1) == 27:
            break
else:
    getDisparity()


cv2.waitKey(0)
cv2.destroyAllWindows()