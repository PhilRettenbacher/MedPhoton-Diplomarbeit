from stereovision import calibration
from ImagingApi import ImagingApi
import os
import cv2

cam = ImagingApi.CameraApi(False, (1,0))

picture1, picture2 = cam.getPicture()

print(picture1.shape)
calibrator = calibration.StereoCalibrator(8, 6, 3, (picture1.shape[0],picture1.shape[1]));

cv2.waitKey(2000)

for x in range(20):
    picture1, picture2 = cam.getPicture()
    calibrator.add_corners((picture1, picture2));
    print("Picture_"+str(x)+" taken")
    cv2.imshow("Picture1", picture1)
    cv2.imshow("Picture2", picture2)
    cv2.waitKey(1000)

calibration = calibrator.calibrate_cameras()

avg_error = calibrator.check_calibration(calibration)

calibration.export(os.getcwd()+"/CalData")
print(avg_error)
