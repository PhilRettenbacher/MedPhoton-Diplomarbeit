import cv2
from matplotlib import pyplot as plt
import numpy as np
from glob import glob

_3d_points = []
_2d_points = []

x,y=np.meshgrid(range(7),range(6))

world_points=np.hstack((x.reshape(42,1),y.reshape(42,1),np.zeros((42,1)))).astype(np.float32)

img_paths = glob('TestImgData/*.jpg')  # get paths of all all images
for path in img_paths:
    im = cv2.imread(path)
    ret, corners = cv2.findChessboardCorners(im, (7, 6))

    if ret:  # add points only if checkerboard was correctly detected:
        _2d_points.append(corners)  # append current 2D points
        _3d_points.append(world_points)  # 3D points are always the same


    #print("Ret:", ret)
    #print("Mtx:", mtx, " ----------------------------------> [", mtx.shape, "]")
    #print("Dist:", dist, " ----------> [", dist.shape, "]")
    #print("rvecs:", rvecs, " --------------------------------------------------------> [", rvecs[0].shape, "]")
    #print("tvecs:", tvecs, " -------------------------------------------------------> [", tvecs[0].shape, "]")

x,y=np.meshgrid(range(7),range(6))
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(_3d_points, _2d_points, (im.shape[1], im.shape[0]), None, None)
print (world_points)

all_right_corners = []
all_left_corners = []
all_3d_points = []
idx = [1, 3, 6, 12, 14]  # we use only some image pairs
valid_idxs = []  # we will also keep an list of valid indices, i.e., indices for which the procedure succeeded
for i in idx:
    im_left = cv2.imread("TestImgData/left%02d.jpg" % i)  # load left and right images
    im_right = cv2.imread("TestImgData/right%02d.jpg" % i)

    ret_left, left_corners = cv2.findChessboardCorners(im_left, (7, 6))
    ret_right, right_corners = cv2.findChessboardCorners(im_right, (7, 6))

    if ret_left and ret_right:  # if both extraction succeeded
        valid_idxs.append(i)
        all_right_corners.append(right_corners)
        all_left_corners.append(left_corners)
        all_3d_points.append(world_points)



print (len(all_right_corners))
print (len(all_left_corners))
print (len(all_3d_points))

print (all_right_corners[0].shape)
print (all_left_corners[0].shape)
print (all_3d_points[0].shape)

print (all_right_corners[0].reshape(-1,2)[0])

retval, _, _, _, _, R, T, E, F=cv2.stereoCalibrate(all_3d_points, all_left_corners, all_right_corners, mtx,dist,mtx, dist,(im.shape[0],im.shape[0]), flags=cv2.CALIB_FIX_INTRINSIC)

selected_image=2
left_im=cv2.imread("TestImgData/left%02d.jpg"%valid_idxs[selected_image])
right_im=cv2.imread("TestImgData/right%02d.jpg"%valid_idxs[selected_image])
left_corners=all_left_corners[selected_image].reshape(-1,2)
right_corners=all_right_corners[selected_image].reshape(-1,2)

plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(left_im)
plt.subplot(122)
plt.imshow(right_im)
plt.show()

cv2.circle(left_im,(left_corners[0,0],left_corners[0,1]),10,(0,0,255),10)
cv2.circle(right_im,(right_corners[0,0],right_corners[0,1]),10,(0,0,255),10)

plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(left_im[...,::-1])
plt.subplot(122)
plt.imshow(right_im[...,::-1])
plt.show()

F, mask=cv2.findFundamentalMat(left_corners, right_corners, cv2.FM_RANSAC, 2)

lines_right = cv2.computeCorrespondEpilines(left_corners, 1,F)
print (lines_right.shape)
lines_right=lines_right.reshape(-1,3) #reshape for convenience
print (lines_right.shape)
print(lines_right)

def drawLine(line, image, side):
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
    cv2.line(image, (int(x0), int(y0)), (int(x1), int(y1)), (0, 255, 255), 3)  # draw the image in yellow with line_width=3

for line in lines_right:
    drawLine(line, right_im, 0)

lines_left = cv2.computeCorrespondEpilines(right_corners, 2,F)
lines_left=lines_left.reshape(-1,3)

drawLine(lines_left[0],left_im, 1)


for line in lines_left:
    drawLine(line, left_im, 1)


plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(left_im[...,::-1])
plt.subplot(122)
plt.imshow(right_im[...,::-1])
plt.show()


plt.figure(figsize=(10,4))
plt.subplot(121)
plt.imshow(left_im[...,::-1])
plt.subplot(122)
plt.imshow(right_im[...,::-1])
plt.show()