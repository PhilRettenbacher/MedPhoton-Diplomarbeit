import cv2
from matplotlib import pyplot as plt
import numpy as np
from glob import glob
import numpy as np
from ImagingApi import ImagingApi

x,y=np.meshgrid(range(8),range(6))
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

world_points=np.hstack((x.reshape(8*6,1),y.reshape(8*6,1),np.zeros((8*6,1)))).astype(np.float32)

imLeft = cv2.imread("TestingImagesActual/image_L_00.jpg")
imRight = cv2.imread("TestingImagesActual/image_R_00.jpg")

#_3d_points=[]
#_2d_points=[]

#img_paths = glob('TestingImagesActual\*[R]*.jpg')  # get paths of all all images
#for path in img_paths:
#    im = cv2.imread(path)
#    ret, corners = cv2.findChessboardCorners(im, (8, 6))
#
#    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#
#    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
#
#    print(path)
#
#    if ret:  # add points only if checkerboard was correctly detected:
#        _2d_points.append(corners)  # append current 2D points
#        _3d_points.append(world_points)  # 3D points are always the same
#        print("found")

#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(_3d_points, _2d_points, (imLeft.shape[1],imLeft.shape[0]), None, None)
#print("Mean Reprojection Error: " + str(ret))

#plt.subplot(121)
#plt.imshow(imRight[...,::-1])
#plt.subplot(122)
#plt.imshow(cv2.undistort(imRight, mtx, dist)[...,::-1])
#plt.show()

img_L_paths = glob('TestingImagesActual\*[L]*.jpg')
img_R_paths = glob('TestingImagesActual\*[R]*.jpg')

_3d_points = []
_2d_points_L=[]
_2d_points_R=[]

for path in glob('TestingImagesActual\*.jpg'):
    im = cv2.imread(path)
    ret, corners = cv2.findChessboardCorners(im, (8, 6))

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print (path)
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    print(path)

    if ret:  # add points only if checkerboard was correctly detected:
        if(path in img_L_paths):
            _2d_points_L.append(corners)  # append current 2D points
            _3d_points.append(world_points)
        else:
            _2d_points_R.append(corners)
        print("found")
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(_3d_points, _2d_points_L, (imLeft.shape[1],imLeft.shape[0]), None, None)
print("Mean Reprojection Error Left: " + str(retL))

retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(_3d_points, _2d_points_R, (imRight.shape[1],imRight.shape[0]), None, None)
print("Mean Reprojection Error Right: " + str(retR))

retval, _, _, _, _, R, T, E, F=cv2.stereoCalibrate(_3d_points, _2d_points_L, _2d_points_R, mtxL,distL,mtxR, distR,(imLeft.shape[1],imLeft.shape[0]), flags=cv2.CALIB_FIX_INTRINSIC)

print(retval)
selected_image = 10
left_im=cv2.imread("TestingImagesActual\image_L_"+str(selected_image).zfill(2)+".jpg")
left_im = cv2.undistort(left_im, mtxL, distL)#[...,::-1]
right_im=cv2.imread("TestingImagesActual\image_R_"+str(selected_image).zfill(2)+".jpg")
right_im = cv2.undistort(right_im, mtxR, distR)#[...,::-1]
left_corners=_2d_points_L[selected_image].reshape(-1,2)
right_corners=_2d_points_R[selected_image].reshape(-1,2)


def drawLine(line, image, id, count):
    a = line[0]
    b = line[1]
    c = line[2]

    # ax+by+c -> y=(-ax-c)/b
    # define an inline function to compute the explicit relationship
    def y(x): return (-a * x - c) / b

    x0 = 0  # starting x point equal to zero
    x1 = image.shape[1]  # ending x point equal to the last column of the image

    y0 = y(x0)  # corresponding y points
    y1 = y(x1)

    # draw the line
    cv2.line(image, (x0, int(y0)), (x1, int(y1)), (id/(count+0.)*255, 255-id/(count+0.)*255, 0), 2)  # draw the image in yellow with line_width=3

lines_right = cv2.computeCorrespondEpilines(_2d_points_L[selected_image], 1,F)
lines_right=lines_right.reshape(-1,3) #reshape for convenience
for x in range(0, len(lines_right)):
    drawLine(lines_right[x], right_im, x, len(lines_right))


lines_left = cv2.computeCorrespondEpilines(_2d_points_R[selected_image], 2,F)
lines_left=lines_left.reshape(-1,3) #reshape for convenience

for x in range(0, len(lines_left)):
    drawLine(lines_left[x], left_im, x, len(lines_left))

print(len(lines_left))

cv2.circle(left_im,(left_corners[0,0],left_corners[0,1]),10,(0,255,255),10)
cv2.circle(right_im,(right_corners[0,0],right_corners[0,1]),10,(0,255,255),10)



#rectify

R1, R2, P1, P2, Q, _, _= cv2.stereoRectify(mtxL, distL, mtxR, distR, (imLeft.shape[1],imLeft.shape[0]), R, T)

map1_x,map1_y=cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, (left_im.shape[1],left_im.shape[0]), cv2.CV_32FC1)
map2_x,map2_y=cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, (left_im.shape[1],left_im.shape[0]), cv2.CV_32FC1)

rect_im_left = cv2.imread("TestingImages\image_L_5.jpg");
rect_im_right = cv2.imread("TestingImages\image_R_5.jpg");

im_left_remapped=cv2.remap(rect_im_left,map1_x,map1_y,cv2.INTER_CUBIC)
im_right_remapped=cv2.remap(rect_im_right,map2_x,map2_y,cv2.INTER_CUBIC)

plt.imshow(im_left_remapped)
plt.show()
out=np.hstack((im_left_remapped,im_right_remapped))

plt.figure(figsize=(10,4))
#plt.imshow(out[...,::-1])
#plt.show()

for i in range(0, out.shape[0], 30):
    cv2.line(out, (0, i), (out.shape[1], i), (0, 255, 255), 3)

plt.figure(figsize=(10, 4))
plt.imshow(out[..., ::-1])
plt.show()

im_left_remapped = cv2.cvtColor(im_left_remapped, cv2.COLOR_BGR2GRAY)
im_right_remapped = cv2.cvtColor(im_right_remapped, cv2.COLOR_BGR2GRAY)

stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=12, speckleWindowSize=50, speckleRange=15, P2 = 1500,)
disparity = stereo.compute(im_left_remapped,im_right_remapped)
plt.imshow(disparity/1024,'gray')
plt.show()
cam = ImagingApi.CameraApi(False, (1, 0))
while True:


    frame1, frame2 = cam.getPicture()
    im_left_remapped = cv2.remap(frame1, map1_x, map1_y, cv2.INTER_CUBIC)
    im_right_remapped = cv2.remap(frame2, map2_x, map2_y, cv2.INTER_CUBIC)

    #plt.imshow(im_left_remapped)
    #plt.show()
    #out = np.hstack((im_left_remapped, im_right_remapped))

    #plt.figure(figsize=(10, 4))
    # plt.imshow(out[...,::-1])
    #plt.show()

    #for i in range(0, out.shape[0], 30):
    #    cv2.line(out, (0, i), (out.shape[1], i), (0, 255, 255), 3)

    #plt.figure(figsize=(10, 4))
    # plt.imshow(out[..., ::-1])
    #plt.show()

    im_left_remapped = cv2.cvtColor(im_left_remapped, cv2.COLOR_BGR2GRAY)
    im_right_remapped = cv2.cvtColor(im_right_remapped, cv2.COLOR_BGR2GRAY)

    cv2.imshow("L", im_left_remapped)
    cv2.imshow("R", im_right_remapped)

    stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=12, speckleWindowSize=50, speckleRange=15, P2=1500, )
    disparity = stereo.compute(im_left_remapped, im_right_remapped)
    #plt.imshow(disparity / 1024, 'gray')
    #plt.show()
    cv2.imshow("disparity", disparity / 1024. + 16)
    cv2.waitKey(1)


