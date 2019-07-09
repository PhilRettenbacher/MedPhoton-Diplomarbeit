import numpy as np
import cv2
import glob
#cap = cv2.VideoCapture('http://192.168.43.81:8081/')
#cap2 = cv2.VideoCapture('http://192.168.43.81:8082/')

isMatrixSet = False

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(1);

while True:
  ret, frame = cap.read()
  # ret2, frame2 = cap2.read()

  # cv2.namedWindow("Video")
  # cv2.imshow('Video', frame)
  # cv2.namedWindow("Video2")
  # cv2.imshow("Video2", frame2)

  img = frame
  cv2.imshow("window", img);
  if cv2.waitKey(1) == 32:


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
      print("Checkerboard found");
      objpoints.append(objp)

      corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
      imgpoints.append(corners2)

      if not isMatrixSet:
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        np.savez("B.npz", ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs);
        isMatrixSet = True;
      with np.load('B.npz') as X:
        mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
        # undistort
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv2.imshow('img', dst)

    #cv2.waitKey(500)
  if cv2.waitKey(1) == 27:
    exit(0)


