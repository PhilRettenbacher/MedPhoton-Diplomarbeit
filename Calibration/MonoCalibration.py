import cv2
import numpy as np


class MonoCalibrator:

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def __init__(self, checkerSize, imgShape):
        self.checkerSize = checkerSize                      #dimension of the checkerboard (x, y)
        self.imgShape = imgShape                            #image shape
        self.imgSize = (imgShape[1], imgShape[0])           #image shape, but values are swapped (some openCV functions require it)
        self.checkerCount = checkerSize[0]*checkerSize[1]   #number of fields
        self.x, self.y = np.meshgrid(range(self.checkerSize[0]), range(self.checkerSize[1]))
        self.world_points = np.hstack((self.x.reshape(self.checkerCount, 1),
                                       self.y.reshape(self.checkerCount, 1),
                                       np.zeros((self.checkerCount, 1)))).astype(np.float32)    #generates 3d coordinates for every corner
        self.Points2D = []                                   #position of the corners in image space
        self.Points3D = []                                   #position of the corners in world space

    #adds an image to the calibration
    def addCheckerBoard(self, img, show = False, delay = 1):
        #Find corners
        ret, corners = cv2.findChessboardCorners(img, self.checkerSize)

        #if all corners where found (ret == True)
        if (ret):

            #convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #enhance to subpixel accuracy
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)

            #show the found chessboardcorners (if show is True)
            if(show):
                im = img.copy()

                cv2.imshow("checkerBoard", cv2.drawChessboardCorners(im, self.checkerSize, corners, ret))

                cv2.waitKey(delay)


            self.Points2D.append(corners)  # append current 2D points
            self.Points3D.append(self.world_points) # append 3D points (they are always the same)

        return (ret, corners)

    def calibrateCamera(self):
        #calibrate the cameras
            #ret: mean projection error, indicates quality of the calibration (should be below 1)
            #mtx: camera matrix
            #dist: distortion parameters
            #rvecs, tvecs rotation and translation vectors (relative to the chessboard, not required)
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.Points3D, self.Points2D,
                                                                (self.imgSize), None, None)
    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist)
    def getCalibData(self):
        #collects calibration data into a tuple, used for saving
        return (self.ret, self.mtx, self.dist, self.rvecs, self.tvecs)