import cv2
import numpy as np
import glob

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW);

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

# Load previously saved data
with np.load('B.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((8*6,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

#for fname in glob.glob('Cam1Footage/*.jpg'):
#    img = cv2.imread(fname)
while (True):
    ret, gray = cap.read()
    gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (8,6),None)
    cv2.imshow('ha', gray)

    if ret == True:
         corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

         # Find the rotation and translation vectors.
         retvalue, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

         # project 3D points to image plane
         imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

         img = draw(gray,corners2,imgpts)
         cv2.imshow('img',img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
