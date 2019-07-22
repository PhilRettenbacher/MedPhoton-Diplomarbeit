import cv2
import numpy as np


class MonoCalibrator:
    Points2D = []
    Points3D = []

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def __init__(self, checkerSize, imgShape):
        self.checkerSize = checkerSize
        self.imgShape = imgShape
        self.imgSize = (imgShape[1], imgShape[0])
        self.checkerCount = checkerSize[0]*checkerSize[1]
        self.x, self.y = np.meshgrid(range(self.checkerSize[0]), range(self.checkerSize[1]))
        self.world_points = np.hstack((self.x.reshape(self.checkerCount, 1), self.y.reshape(self.checkerCount, 1), np.zeros((self.checkerCount, 1)))).astype(np.float32)

    def addCheckerBoard(self, img, show = False, delay = 1):
        ret, corners = cv2.findChessboardCorners(img, self.checkerSize)

        if (ret):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # enhance acccuracy
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)

            if(show):
                im = img.copy()
                cv2.imshow("checkerBoard", cv2.drawChessboardCorners(im, self.checkerSize, corners, ret))
                cv2.waitKey(delay)

            self.Points2D.append(corners)  # append current 2D points
            self.Points3D.append(self.world_points)

        return (ret, corners)

    def calibrateCamera(self):
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.Points3D, self.Points2D,
                                                                (self.imgSize), None, None)
    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist)
    def getCalibData(self):
        return (self.ret, self.mtx, self.dist, self.rvecs, self.tvecs)