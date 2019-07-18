import cv2
from matplotlib import pyplot as plt
import numpy as np
import numpy as np

class StereoImager:
    _3d_points = []
    _2d_points_L = []
    _2d_points_R = []





    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


    def __init__(self, shape0, shape1, checkX, checkY, stereoBM):
        print("Initialize StereoImager")
        self.shape0 = shape0
        self.shape1 = shape1

        self.checkX = checkX
        self.checkY = checkY
        self.x, self.y = np.meshgrid(range(checkX), range(checkY))

        self.checkCount = self.checkX*self.checkY

        self.world_points = np.hstack((self.x.reshape(self.checkCount, 1), self.y.reshape(self.checkCount, 1), np.zeros((self.checkCount, 1)))).astype(np.float32)
        self.stereoBM = stereoBM

    def addCheckerboard(self, imLeft, imRight):
        retL, cornersL = cv2.findChessboardCorners(imLeft, (self.checkX, self.checkY))
        retR, cornersR = cv2.findChessboardCorners(imRight, (self.checkX, self.checkY))

        if(retL and retR):
            grayL = cv2.cvtColor(imLeft, cv2.COLOR_BGR2GRAY)
            grayR = cv2.cvtColor(imRight, cv2.COLOR_BGR2GRAY)

            #enhance acccuracy
            cornersL = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), self.criteria)
            cornersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), self.criteria)

            self._2d_points_R.append(cornersR)
            self._2d_points_L.append(cornersL)  # append current 2D points
            self._3d_points.append(self.world_points)

            return True
        else:
            return False

    def calibrateCamerasIndividual(self):
        self.retL, self.mtxL, self.distL, self.rvecsL, self.tvecsL = cv2.calibrateCamera(self._3d_points, self._2d_points_L,
                                                                (self.shape1, self.shape0), None, None)
        self.retR, self.mtxR, self.distR, self.rvecsR, self.tvecsR = cv2.calibrateCamera(self._3d_points, self._2d_points_R,
                                                                (self.shape1, self.shape0), None, None)
    def meanProjectionErrorIndividual(self):
        return (self.retL, self.retR)

    def calibrateCameras(self):
        self.retval, _, _, _, _, self.R, self.T, self.E, self.F = cv2.stereoCalibrate(self._3d_points, self._2d_points_L, self._2d_points_R, self.mtxL, self.distL, self.mtxR,
                                                             self.distR, (self.shape1, self.shape0),
                                                             flags=cv2.CALIB_FIX_INTRINSIC)
    def meanProjectionError(self):
        return self.retval

    def calcRectify(self):
        self.R1, self.R2, self.P1, self.P2, self.Q, _, _ = cv2.stereoRectify(self.mtxL, self.distL, self.mtxR, self.distR, (self.shape1, self.shape0), self.R, self.T)
        self.map1_x, self.map1_y = cv2.initUndistortRectifyMap(self.mtxL, self.distL, self.R1, self.P1, (self.shape1, self.shape0),
                                                     cv2.CV_32FC1)
        self.map2_x, self.map2_y = cv2.initUndistortRectifyMap(self.mtxR, self.distR, self.R2, self.P2, (self.shape1, self.shape0),
                                                     cv2.CV_32FC1)

    def undistort(self, img, isLeft):
        if(isLeft):
            return cv2.undistort(img, self.mtxL, self.distL)
        else:
            return cv2.undistort(img, self.mtxR, self.distR)

    def rectifyAndRemap(self, img, isLeft):
        img = cv2.remap(img, self.map1_x if isLeft else self.map2_x,
                             self.map1_y if isLeft else self.map2_y, cv2.INTER_CUBIC)

        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def calcDisparityRectified(self, imLeft, imRight):
        return self.stereoBM.compute(imLeft,imRight)

    def calibrateFull(self):
        self.calibrateCamerasIndividual()
        self.calibrateCameras()
        self.calcRectify()

    def calcDisparity(self, imLeft, imRight):
        imLeft = self.rectifyAndRemap(imLeft, True)
        imRight = self.rectifyAndRemap(imRight, False)
        return self.calcDisparityRectified(imLeft, imRight)