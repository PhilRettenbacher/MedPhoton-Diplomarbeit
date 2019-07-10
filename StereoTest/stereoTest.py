from stereovision import calibration
from ImagingApi import ImagingApi
import os
import cv2

cam = ImagingApi.CameraApi(False, (1,2))

picture1, picture2 = cam.getPicture()

calibrator = calibration.StereoCalibrator(8, 6, 3, (picture1.shape[0],picture1.shape[1]));

for x in range(30):
    calibrator.add_corners((picture1, picture2));
    picture1, picture2 = cam.getPicture()
    print("Picture_"+str(x)+" taken")
    cv2.waitKey(2000)

calibration = calibrator.calibrate_cameras()

avg_error = calibrator.check_calibration(calibration)

calibration.export(os.getcwd()+"/CalData")
print(avg_error)
