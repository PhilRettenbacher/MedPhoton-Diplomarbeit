from Calibration import StereoCalibration
from Calibration import MonoCalibration
import glob
from time import monotonic
import cv2
import numpy

def main(imgPaths, savePaths, doMono=True, doStereo=True, checkerBoardShape=(8, 6)):
    print("Start Calibration...")

    startCalib = monotonic()

    ######################
    ## Mono Calibration ##
    ######################

    monoCalibData = None
    stereoCalibData = None

    if(doMono):
        startCalibMono = monotonic()
        print("Starting left mono Calibration...")
        calMonoL = calibMono(imgPaths[0], checkerBoardShape)
        print("Left mono Calibration finished: " + str(monotonic() - startCalibMono) + " s...")

        startCalibR = monotonic()
        print("Starting right mono Calibration...")
        calMonoR = calibMono(imgPaths[1], checkerBoardShape)
        print("Right mono Calibration finished: " + str(monotonic() - startCalibR) + " s...")

        print("Saving calibration data...")
        numpy.save(savePaths[0], calMonoL)
        numpy.save(savePaths[1], calMonoR)

        monoCalibData = (calMonoL, calMonoR)
        print("Mono Calibration accuracy...")
        print("---Left:  " + str(calMonoL[0]))
        print("---Right: " + str(calMonoR[0]))
        print("Mono Calibration finished: " + str(monotonic() - startCalibMono) + " s...")
    else:
        print("Fetching mono Calibration data")
        calMonoL = numpy.load(savePaths[0], allow_pickle=True)
        calMonoR = numpy.load(savePaths[1], allow_pickle=True)
        monoCalibData = (calMonoL, calMonoR)

    if(doStereo):
        startCalibStereo = monotonic()
        print("Starting stereo Calibration...")
        stereoCalibData = calibStereo((imgPaths[2], imgPaths[3]), checkerBoardShape, monoCalibData)
        numpy.save(savePaths[2], numpy.array(stereoCalibData[0]))
        numpy.save(savePaths[3], numpy.array(stereoCalibData[1]))

        print("Stereo Calibration finished: " + str(monotonic() - startCalibStereo) + " s...")
    else:
        print("Fetching stereo Calibration data")
        calStereoX = numpy.load(savePaths[2], allow_pickle=True)
        calStereoY = numpy.load(savePaths[3], allow_pickle=True)
        stereoCalibData = (calStereoX, calStereoY)

    print("Calibration finished: " + str(monotonic()-startCalib) + " s...")
    return (monoCalibData, stereoCalibData)

def calibMono(path, checkerBoardShape):
    imgPaths = glob.glob(path)

    print("Found " + str(len(imgPaths)) + " images:")

    if(len(imgPaths)==0):
        print("No images found for monocalibration!")
        return None
    calib = MonoCalibration.MonoCalibrator(checkerBoardShape, cv2.imread(imgPaths[0]).shape[:-1])
    for imgPath in imgPaths:
        img = cv2.imread(imgPath)
        calib.addCheckerBoard(img)
    calib.calibrateCamera()
    return calib.getCalibData()

def calibStereo(paths, checkerBoardShape, monoCalib):
    imgPathsL = glob.glob(paths[0])
    imgPathsR = glob.glob(paths[1])

    if(len(imgPathsL)!=len(imgPathsR)):
        print("Count of images for stereocalibration do not match up!")
        return None
    if(len(imgPathsL)==0):
        print("No images found for stereocalibration!")
        return None

    print("Found " + str(len(imgPathsL)) + " images:")

    calib = StereoCalibration.StereoCalibrator((8, 6), cv2.imread(imgPathsL[0]).shape[:-1], monoCalib[0], monoCalib[1])

    for x in range(0, len(imgPathsL)):
        imgL = cv2.imread(imgPathsL[x])
        imgR = cv2.imread(imgPathsR[x])
        calib.addCheckerBoard(imgL, imgR, calibrated=False)

    calib.calibrate(shearing=True)
    return calib.getCalcData()





'''main(("CalibLTest/*.jpg", "CalibRTest/*.jpg", "stereoL/*.jpg", "stereoR/*.jpg"),
     ("CalibResults/LCalib.npy", "CalibResults/RCalib.npy", "CalibResults/StereoX.npy", "CalibResults/StereoY.npy"),
     doMono=True, doStereo=True)'''
