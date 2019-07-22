import cv2
import numpy as np
from Calibration import MonoCalibration

class StereoCalibrator:
    L2DPoints = []
    R2DPoints = []

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def __init__(self, checkerSize, imgShape, calibL, calibR):
        self.checkerSize = checkerSize
        self.imgShape = imgShape
        self.imgSize = (imgShape[1], imgShape[0])
        self.checkerCount = checkerSize[0]*checkerSize[1]
        self.x, self.y = np.meshgrid(range(self.checkerSize[0]), range(self.checkerSize[1]))
        self.world_points = np.hstack((self.x.reshape(self.checkerCount, 1), self.y.reshape(self.checkerCount, 1), np.zeros((self.checkerCount, 1)))).astype(np.float32)

        self.calibL = calibL
        self.calibR = calibR
        self.INTERPOLATION = cv2.INTER_LINEAR

        self.internalMonoCal = MonoCalibration.MonoCalibrator(checkerSize, imgShape)

    def addCheckerBoard(self, imgL, imgR, calibrated, show = False, delay = 1):
        if (not calibrated):
            imgL = self.undistort(imgL, True)
            imgR = self.undistort(imgR, True)

        self.internalMonoCal.addCheckerBoard(imgL)

        retL, cornersL = cv2.findChessboardCorners(imgL, self.checkerSize)
        retR, cornersR = cv2.findChessboardCorners(imgR, self.checkerSize)

        if (retL and retR):
            grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
            grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

            # enhance acccuracy
            cornersL = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), self.criteria)
            cornersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), self.criteria)

            if(show):
                l = imgL.copy()
                r = imgR.copy()
                cv2.imshow("l", cv2.drawChessboardCorners(l, self.checkerSize, cornersL, retL))
                cv2.imshow("r", cv2.drawChessboardCorners(r, self.checkerSize, cornersR, retR))
                cv2.waitKey(delay)

            self.R2DPoints.append(cornersR)
            self.L2DPoints.append(cornersL)  # append current 2D points

        return (retL, retR, cornersL, cornersR)

    def undistort(self, img, isLeft):
        if(isLeft):
            return cv2.undistort(img, self.calibL[1], self.calibL[2])
        else:
            return cv2.undistort(img, self.calibR[1], self.calibR[2])


    def calibrate(self, shearing=True):
        self.internalMonoCal.calibrateCamera()
        calData = self.internalMonoCal.getCalibData()
        K = calData[1]
        d = calData[2]
        ##### ##### ##### ##### #####
        ##### Compute Fundamental matrix
        ##### ##### ##### ##### #####

        x1 = np.array(self.L2DPoints)
        x1 = x1.reshape((x1.shape[0] * x1.shape[1], 1, 2))

        x2 = np.array(self.R2DPoints)
        x2 = x2.reshape((x2.shape[0] * x2.shape[1], 1, 2))

        F, F_mask = cv2.findFundamentalMat(x1, x2, method=cv2.FM_RANSAC, ransacReprojThreshold=5)

        # Select only inlier points
        F_mask = F_mask.flatten()
        x1 = x1[F_mask == 1]
        x2 = x2[F_mask == 1]

        # Rectification based on found Fundamental matrix

        #image_shape = (image1.shape[0], image1.shape[1])
        #(height, width) = image_shape
        #image_size = (width, height)  # Note: image_size is not image_shape

        # Calculate Homogeneous matrix transform given features and fundamental matrix

        retval, H1, H2 = cv2.stereoRectifyUncalibrated(x1.ravel(), x2.ravel(), F, self.imgSize, threshold=5)

        if (retval == False):
            print("ERROR: stereoRectifyUncalibrated failed")
            return None

        # Apply a shearing transform to homography matrices
        if shearing:
            S = self.rectify_shearing(H1, H2, self.imgSize[0], self.imgSize[1])
            H1 = S.dot(H1)

        # Compute the rectification transform
        K_inverse = np.linalg.inv(K)
        R1 = K_inverse.dot(H1).dot(K)
        R2 = K_inverse.dot(H2).dot(K)

        self.mapx1, self.mapy1 = cv2.initUndistortRectifyMap(K, d, R1, K, self.imgSize, cv2.CV_16SC2)
        self.mapx2, self.mapy2 = cv2.initUndistortRectifyMap(K, d, R2, K, self.imgSize, cv2.CV_16SC2)

        # Find an unused colour to build a border mask
        # Note: Assuming that the union of both image intensity sets do not exhaust the 8 bit range
        # Fortunately, if the set is empty, set.pop() will throw a runtime error

        #palette1 = set(image1.flatten())
        #palette2 = set(image2.flatten())

        #colours = set(range(256))

        # key1 = colours.difference(palette1).pop()
        # key2 = colours.difference(palette2).pop()

        ##### ##### ##### ##### #####
        ##### Apply Rectification Transform
        ##### ##### ##### ##### #####

        # TODO: Determine which interpolation method is best
        #INTERPOLATION = cv2.INTER_LINEAR  # cv2.INTER_LINEAR

        #rectified1 = cv2.remap(image1, mapx1, mapy1,
                               #interpolation=INTERPOLATION,
                               #borderMode=cv2.BORDER_CONSTANT,
                               #)

        #rectified2 = cv2.remap(image2, mapx2, mapy2,
                               #interpolation=INTERPOLATION,
                               #borderMode	= cv2.BORDER_CONSTANT,
                               #)

        # Build the mask, used for cropping out noise

        #rectified1_mask = numpy.ndarray(image_shape, dtype = bool)
        #rectified2_mask = numpy.ndarray(image_shape, dtype = bool)

        #rectified1_mask.fill(True)
        #rectified2_mask.fill(True)

        # rectified1_mask[rectified1 == key1] = False
        # rectified2_mask[rectified2 == key2] = False

        # numpy.save("mask1.npy", rectified1_mask)
        # numpy.save("mask2.npy", rectified2_mask)

        # All done!

        #return rectified1, rectified2, rectified1_mask, rectified2_mask, mapx1, mapy1, mapx2, mapy2

    def rectifyImg(self, img, isLeft):
        if(isLeft):
            return(cv2.remap(img, self.mapx1, self.mapy1, interpolation=self.INTERPOLATION, borderMode=cv2.BORDER_CONSTANT))
        else:
            return(cv2.remap(img, self.mapx2, self.mapy2, interpolation=self.INTERPOLATION, borderMode=cv2.BORDER_CONSTANT))


    def rectify_shearing(self, H1, H2, image_width, image_height):

        ##### ##### ##### ##### #####
        ##### CREDIT
        ##### ##### ##### ##### #####

        # Loop & Zhang - via literature
        #	* http://scicomp.stackexchange.com/questions/2844/shearing-and-hartleys-rectification
        # TH. - via stackexchange user
        # 	* http://scicomp.stackexchange.com/users/599/th
        #	* http://scicomp.stackexchange.com/questions/2844/shearing-and-hartleys-rectification

        ##### ##### ##### ##### #####
        ##### PARAMETERS
        ##### ##### ##### ##### #####

        # Let H1 be the rectification homography of image1 (ie. H1 is a homogeneous space)
        # Let H2 be the rectification homography of image2 (ie. H2 is a homogeneous space)
        # image_width, image_height be the dimensions of both image1 and image2

        ##### ##### ##### ##### #####

        """
        Compute shearing transform than can be applied after the rectification transform to reduce distortion.
        Reference:
            http://scicomp.stackexchange.com/questions/2844/shearing-and-hartleys-rectification
            "Computing rectifying homographies for stereo vision" by Loop & Zhang
        """

        w = image_width
        h = image_height

        '''
        Loop & Zhang use a shearing transform to reduce the distortion
        introduced by the projective transform that mapped the epipoles to infinity
        (ie, that made the epipolar lines parallel).
        Consider the shearing transform:
                | k1 k2 0 |
        S	=	| 0  1  0 |
                | 0  0  1 |
        Let w and h be image width and height respectively.
        Consider the four midpoints of the image edges:
        '''

        a = np.float32([(w - 1) / 2.0, 0, 1])
        b = np.float32([(w - 1), (h - 1) / 2.0, 1])
        c = np.float32([(w - 1) / 2.0, (h - 1), 1])
        d = np.float32([0, (h - 1) / 2.0, 1])

        '''
        According to Loop & Zhang:
        "... we attempt to preserve perpendicularity and aspect ratio of the lines bd and ca"
        '''

        '''
        Let H be the rectification homography and,
        Let a' = H*a be a point in the affine plane by dividing through so that a'2 = 1
        Note: a'2 is the third component, ie, a' = (a'[0], a'1, a'2))
        '''

        # Note: *.dot is a form of matrix*vector multiplication in numpy
        # So a_prime = H*a such that a_prime[2] = 1 (hence the use of homogeneous_to_euclidean function)
        print(a)
        a_prime = cv2.convertPointsFromHomogeneous(np.array([H1.dot(a)])).squeeze()
        b_prime = cv2.convertPointsFromHomogeneous(np.array([H1.dot(b)])).squeeze()
        c_prime = cv2.convertPointsFromHomogeneous(np.array([H1.dot(c)])).squeeze()
        d_prime = cv2.convertPointsFromHomogeneous(np.array([H1.dot(d)])).squeeze()


        ''' Let x = b' - d' and y = c' - a' '''
        x = b_prime - d_prime
        y = c_prime - a_prime

        '''
        According to Loop & Zhang:
            "As the difference of affine points, x and y are vectors in the euclidean image plane.
                Perpendicularity is preserved when (Sx)^T(Sy) = 0, and aspect ratio is preserved if [(Sx)^T(Sx)]/[(Sy)^T(Sy)] = (w^2)/(h^2)"
        '''

        ''' The real solution presents a closed-form: '''

        k1 = (h * h * x[1] * x[1] + w * w * y[1] * y[1]) / (h * w * (x[1] * y[0] - x[0] * y[1]))
        k2 = (h * h * x[0] * x[1] + w * w * y[0] * y[1]) / (h * w * (x[0] * y[1] - x[1] * y[0]))

        ''' Determined by sign (the positive is preferred) '''

        if (k1 < 0):  # Why this?
            k1 *= -1
            k2 *= -1

        return np.float32([
            [k1, k2, 0],
            [0, 1, 0],
            [0, 0, 1]])

    ##### ##### ##### ##### #####

    def getCalcData(self):
        return (self.mapx1, self.mapy1, self.mapx2, self.mapy2)