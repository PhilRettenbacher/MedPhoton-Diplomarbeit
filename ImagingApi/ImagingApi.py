# Version 0.0.2.10
# Author Hannes Schürer

import cv2
import os
from pynput.keyboard import Key, Listener, KeyCode
import time

# Class for managing camera output to the screen and picture storage

class CameraApi:
    saveInDirectory = True
    useWeb = False
    width = 0
    height = 0
    caps = []
    frames = []
    path = ""
    imageCount = 0
    isRunning = False

# The constructor takes 4 parameters(width, height, saveInDirectory saves Pictures in separate folders of each frame if it's true,
# useWeb streams pictures from the attached cameras on the Pi

    def __init__(self, width=640, height=480, saveInDirectory=True, useWeb=False):
        self.saveInDirectory = saveInDirectory
        self.useWeb = useWeb
        self.width = width
        self.height = height
        self.path = os.getcwd()

        deviceNumber = self.lookForDevices(useWeb)

        if deviceNumber > 0:
            print(str(deviceNumber) + " Device(s) found\n")
        else:
            print("No device found\n")
            exit(1)

# readCapture is needed to constantly update the frames array

    def readCapture(self):
        self.frames.clear()
        for c in self.caps:
            ret, frame = c.read()
            self.frames.append(frame)

# getFrames can be used to return a frame array if needed

    def getFrames(self):
        frames = []
        for c in self.caps:
            ret, frame = c.read()
            frames.append(frame)
        return frames

# makeVideo opens a window for each frame and streams the output of all attached cameras in it

    def makeVideo(self):
        self.isRunning = True

        print("End video with escape")
        print("Close frames with 0, 1, 2")
        print("Take picture with space\n")

        while self.isRunning:
            counter = 0
            if len(self.caps) == 0:
                self.isRunning = False

            self.readCapture()

            for f in self.frames:
                try:
                    cv2.imshow(str(counter), f)
                except:
                    print("Camera disconnected")
                    self.caps.pop(counter)
                    cv2.destroyAllWindows()
                    break
                counter += 1

            cv2.waitKey(1)

        self.endProgram()

# key functions: space stores the current picture of the attached cameras
#                the number keys can close the windows if needed
#                with escape you can exit the program

    def keyListener(self):
        def on_press(key):
            if self.isRunning:
                if key == Key.space:
                    if not self.useWeb:
                        self.takePictureLocal()
                    else:
                        self.takePictureWeb()
                if key == KeyCode.from_char('0'):
                    self.destroyCvWindow(0)
                if key == KeyCode.from_char('1'):
                    self.destroyCvWindow(1)
                if key == KeyCode.from_char('2'):
                    self.destroyCvWindow(2)
            if key == Key.esc:
                if self.isRunning:
                    Listener(on_press=on_press).stop()
                    self.isRunning = False
                else:
                    Listener(on_press=on_press).stop()
                    self.endProgram()

        Listener(on_press=on_press).start()

# controls the window closing

    def destroyCvWindow(self, frameNumber):
        try:
            self.caps.pop(frameNumber)
        except:
            print("Frame does not exist")
        cv2.destroyAllWindows()

# returns the amount of the attached cameras

    def getCameraCount(self):
        return len(self.caps)

# takePictureWeb takes picture with the url of the manufacturer

    def takePictureWeb(self):
        count = 0
        tmpFrames = []
        tmpCap1 = (cv2.VideoCapture(
            "http://192.168.199.3:8765/picture/1/current/?_username=admin&_signature=405e3e47c0b54c48c7539decf8437b48bb320e16"))
        found1, frame1 = tmpCap1.read()
        tmpCap2 = (cv2.VideoCapture(
            "http://192.168.199.3:8765/picture/2/current/?_username=admin&_signature=8364b7955ab9bcfe1b2717c91ea1b2d6f2f59a6a"))
        found2, frame2 = tmpCap2.read()
        tmpFrames.append(frame1)
        tmpFrames.append(frame2)
        self.makeDirectory(len(self.caps))
        if found1 & found2:
            for frm in tmpFrames:
                if self.saveInDirectory:
                    cv2.imwrite("./Pictures/Frame_" + str(count) + "/imageFrame_" + str(count) + "_" + str(
                        self.imageCount) + ".jpg", frm)
                else:
                    cv2.imwrite("./Pictures/imageFrame_" + str(count) + "_" + str(self.imageCount) + ".jpg", frm)
                count += 1
            self.imageCount += 1
            print(str(count) + " picture(s) taken, (total of: "+str(self.imageCount)+")")
        return

# takePictureLocal simply writes the current frame in a folder

    def takePictureLocal(self):
        count = 0
        f = []
        f.clear()
        self.makeDirectory(len(self.caps))
        for c in self.caps:
            ret, frame = c.read()
            f.append(frame)

        for frm in f:
            if self.saveInDirectory:
                cv2.imwrite("./Pictures/Frame_" + str(count) + "/imageFrame_" + str(count) + "_" + str(
                    self.imageCount) + ".jpg", frm)
            else:
                cv2.imwrite("./Pictures/imageFrame_" + str(count) + "_" + str(self.imageCount) + ".jpg", frm)
            count += 1
        self.imageCount += count
        print(str(count) + " picture(s) taken, (total of: " + str(self.imageCount) + ")")
        return

# controls the creation of directories

    def makeDirectory(self, frameCount):
        if os.path.exists(os.getcwd() + "/Pictures") & self.saveInDirectory:
            for i in range(0, frameCount):
                if not (os.path.exists(os.getcwd() + "/Pictures/Frame_" + str(i))):
                    os.mkdir(os.getcwd() + "/Pictures/Frame_" + str(i))
            return
        else:
            try:
                self.path = os.getcwd()
                if not os.path.exists(os.getcwd() + "/Pictures"):
                    self.path = self.path + "/Pictures"
                    os.mkdir(self.path)
                if self.saveInDirectory:
                    for i in range(0, frameCount):
                        os.mkdir(self.path + "/Frame_" + str(i))
            except OSError:
                print("Creation of the directory %s failed" % self.path)

# lookForDevices searches for devices that are attached to the computer
# If you don't like to use the web cam, just disable it in the device-manager

    def lookForDevices(self, useWeb):
        portTestRange = 3
        count = 0
        start = -1
        if not useWeb:
            print("Looking for devices(local)")
            for i in range(start, portTestRange):
                cap = (cv2.VideoCapture(i, cv2.CAP_DSHOW))
                found, frame = cap.read()
                if found:
                    count += 1
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    print("Device found on Port " + str(i))
                    self.caps.append(cap)
        else:
            timeDelta = 0
            portTestRange = 3
            start = 1
            print("Looking for devices(web)")
            for i in range(start, portTestRange):
                if not (timeDelta > 4):
                    timestampStart = int(round(time.time()))
                    cap = (cv2.VideoCapture("http://192.168.199.3:808" + str(i) + "/"))
                    timeDelta = (int(round(time.time()))) - timestampStart
                    found, frame = cap.read()
                    if found:
                        count += 1
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                        print("Device found on Port " + str(i))
                        self.caps.append(cap)
                else:
                    print("Could not find device(time exceeded)")
                    return count
        return count

# endProgram simply calls the destructor

    def endProgram(self):
        self.__del__()

# the destructor releases all devices and destroys all windows

    def __del__(self):
        self.frames.clear()
        for c in self.caps:
            c.release()
        cv2.destroyAllWindows()
        print("\nProgram stopped")
        os._exit(1)
