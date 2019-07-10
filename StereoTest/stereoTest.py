from stereovision import calibration
from ImagingApi import ImagingApi
import numpy as np
import cv2

cam = ImagingApi.CameraApi(False, (1,2))

picture1, picture2 = cam.getPicture()

calibrator = calibration.StereoCalibrator(6, 8, 3, (picture1.shape[0],picture1.shape[1]));

for x in range(10):

    calibrator.add_corners((picture1, picture2));
    picture1, picture2 = cam.getPicture()
    print("Picture_"+str(x)+" taken")
    cv2.waitKey(200)

calibration = calibrator.calibrate_cameras()

np.savez("calData.npz", calibration=calibration)

print(calibration)

with np.load('calData.npz') as data:
    a = data['calibration']


avg_error = calibrator.check_calibration(calibration)
