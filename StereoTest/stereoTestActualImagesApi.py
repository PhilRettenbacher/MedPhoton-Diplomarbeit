from StereoUtils import StereoUtils
import cv2

imLeft = cv2.imread("TestingImagesActual/image_L_00.jpg")

stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=12, speckleWindowSize=50, speckleRange=15, P2=1500, )
imager = StereoUtils.StereoImager(imLeft.shape[0], imLeft.shape[1], 8, 6, stereo)

for x in range(0, 11):
    imLeft = cv2.imread("TestingImagesActual/image_L_"+str(x).zfill(2)+".jpg")
    imRight = cv2.imread("TestingImagesActual/image_R_"+str(x).zfill(2)+".jpg")

    imager.addCheckerboard(imLeft, imRight)
#imager.calibrateCamerasIndividual()
#print(imager.meanProjectionErrorIndividual())

#imager.calibrateCameras()
#print(imager.meanProjectionError())

#imager.calcRectify()

imager.calibrateFull()

imLeft = cv2.imread("TestingImages\image_L_5.jpg");
imRight = cv2.imread("TestingImages\image_R_5.jpg");
#imLeft = imager.rectifyAndRemap(imLeft, True)
#imRight = imager.rectifyAndRemap(imRight, False)

cv2.imshow("L", imLeft)
cv2.imshow("R", imRight)

disparity = imager.calcDisparity(imLeft, imRight)
print(disparity)
cv2.imshow("disparity", disparity/1024)

cv2.waitKey(0)