import numpy as np
import cv2
import glob
#cap = cv2.VideoCapture('http://192.168.43.81:8081/')
#cap2 = cv2.VideoCapture('http://192.168.43.81:8082/')

cap = cv2.VideoCapture(1);

x = 6
y = 6

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((x*y,3), np.float32)
objp[:,:2] = np.mgrid[0:x,0:y].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

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
    ret, corners = cv2.findChessboardCorners(gray, (x, y), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
      objpoints.append(objp)

      corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
      imgpoints.append(corners2)

      # Draw and display the corners
      img = cv2.drawChessboardCorners(gray, (x, y), corners2, ret)
      cv2.imshow('img', img)
      cv2.waitKey(500)

      ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

      h, w = img.shape[:2]
      newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

      # undistort
      dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

      # crop the image
      x, y, w, h = roi
      #dst = dst[y:y + h, x:x + w]
      cv2.imshow('calibresult.png', dst)

    #cv2.waitKey(500)
  if cv2.waitKey(1) == 27:
    cv2.destroyAllWindows()
    exit(0)


