from stereovision import calibration
import cv2

calibrator = calibration.StereoCalibrator(6, 8, 3, 0);
frame1 = cv2.imread("image_2.jpg");
frame2 = cv2.imread("image_3.jpg");
print(frame1.shape)
calibrator.add_corners((frame1, frame2));