from Calibration import CameraCalibrationScript
import cv2
from brightnessDetermining import breathingDiagram

#motion snapshot urls (camLeft, camRight)
def main(urls):

    #calibrating the cameras, or loading precalculated values
    calibration = CameraCalibrationScript.main(imgPaths=("CalibLTest/*.jpg", "CalibRTest/*.jpg", "stereoL/*.jpg", "stereoR/*.jpg"), #Paths to the imagefolders (left mono, right mono, left stereo, right stereo)
                                  savePaths=("CalibResults/LCalib.npy", "CalibResults/RCalib.npy", "CalibResults/StereoX.npy",      #Paths to the saved calibration files (will be saved if newly calibrates)
                                  "CalibResults/StereoY.npy"),                                                                      #(left mono, right mono, x stereo, y stereo)
                                  doMono=False, doStereo=False)                                                                     #what calibrations should be done (loads from file if set to False)
    
    #values controlling the cutoff of the image, must be divisable by 16 (cutoff from left ->minDisparity, cutoff from right->maxDisparity-minDisparity)
    minDisp = -16 * 10
    maxDisp = 16 * 10
    
    #setup the block matcher, information about the input values: (http://www.swarthmore.edu/NatSci/mzucker1/opencv-2.4.10-docs/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereosgbm-stereosgbm)
    bm = cv2.StereoSGBM_create(minDisparity=minDisp, numDisparities=maxDisp - minDisp, blockSize=11, P2=4000, P1=1500,
                               uniquenessRatio=4, speckleWindowSize=100, speckleRange=16, disp12MaxDiff=64,
                               preFilterCap=5)

    #setup the diagrams
    diagram = breathingDiagram.BreathingPlotter((breathingDiagram.BreathPlot.WEIGHT_COL_TIME,   #the types you want to show (must be 4),
                                                breathingDiagram.BreathPlot.WEIGHT_ROW_TIME,
                                                breathingDiagram.BreathPlot.AVG_BRIGHT_TIME,
                                                breathingDiagram.BreathPlot.SUM_TIME), 
                                                (480, 640), smooth=True,                        #shape of the image, should the diagrams be smoothed out
                                                frequency=1, autoscale=True)                    #update frequency, automatic scaling

    while (True):
        '''tmpCap1 = (cv2.VideoCapture(urls[0]))
        found1, imLeft = tmpCap1.read()
        tmpCap2 = (cv2.VideoCapture(urls[1]))
        found2, imRight = tmpCap2.read()'''
        imLeft = cv2.imread("stereoL/imageFrame_0_0.jpg")
        imRight = cv2.imread("stereoR/imageFrame_1_0.jpg")

        #undistort and rectify the images
        iml = rectify(undistort(imLeft, calibration[0][1]), calibration[1][0][0], calibration[1][1][0])
        imr = rectify(undistort(imRight, calibration[0][1]), calibration[1][0][1], calibration[1][1][1])

        cv2.imshow("Rectified-L", iml)
        cv2.imshow("Rectified-R", imr)

        #compute the disparity map
        disp = bm.compute(iml, imr)
        
        #Remap the disparity map to a Range of 0-1
        disp = (disp - (minDisp - 1) * 16) / (((maxDisp - minDisp)) * 16)
        
        cv2.imshow("disp", disp)
        cv2.waitKey(1)
        
        #update the diagrams
        diagram.update(disp * 255)

def rectify(img, mapx, mapy):
    return (cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT))
def undistort(img, calib):
    return cv2.undistort(img, calib[1], calib[2])

main(5)