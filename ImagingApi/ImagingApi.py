import cv2
import os
from pynput.keyboard import Key, Listener, Controller, KeyCode
import time


keyboard = Controller()

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

    def __init__(self, width=640, height=480, saveInDirectory=True, useWeb=False):
        self.saveInDirectory = saveInDirectory
        self.isRunning = True
        self.useWeb = useWeb
        self.width = width
        self.height = height
        self.path = os.getcwd()

        deviceNumber = self.lookForDevices(useWeb)

        if(deviceNumber > 0):
            print(str(deviceNumber)+" Device(s) found\n")
        else:
            print("No device found\n")
            exit(1)

    def readCapture(self):
        self.frames.clear()
        for c in self.caps:
             ret, frame = c.read()
             self.frames.append(frame)

    def getFrames(self):
        frames = []
        for c in self.caps:
            ret, frame = c.read()
            frames.append(frame)
        return frames

    def makeVideo(self):
        print("End video with escape")
        print("Close frames with 0, 1, 2")
        print("Take picture with space\n")

        def on_press(key):
            if (key == Key.space):
                if not self.useWeb:
                    self.takePictureLocal()
                else:
                    self.takePictureWeb()
            if key == KeyCode.from_char('0'):
                self.destroyCvWindow(0)
                self.deleteDirectory(0)
            if key == KeyCode.from_char('1'):
                self.destroyCvWindow(1)
                self.deleteDirectory(1)
            if key == KeyCode.from_char('2'):
                self.destroyCvWindow(2)
                self.deleteDirectory(2)
            if key == Key.esc:
                Listener(on_press=on_press).stop()
                self.isRunning=False

        Listener(on_press=on_press).start()

        while self.isRunning:
            counter = 0
            if(len(self.caps)==0):
                self.isRunning=False

            self.readCapture()

            for f in self.frames:
                try:
                    cv2.imshow(str(counter), f)
                except:
                    print("Camera disconnected")
                    self.caps.pop(counter)
                    cv2.destroyAllWindows()
                    break
                counter+=1

            cv2.waitKey(1)

        self.endProgram()

    def destroyCvWindow(self, frameNumber):
        try:
            self.caps.pop(frameNumber)
        except:
            print("Frame does not exist")
        cv2.destroyAllWindows()

    def getCameraCount(self):
        return len(self.caps)

    def takePictureWeb(self):
        count = 0
        tmpFrames = []
        tmpCap1 = (cv2.VideoCapture("http://192.168.199.3:8765/picture/1/current/?_username=admin&_signature=405e3e47c0b54c48c7539decf8437b48bb320e16"))
        found1, frame1 = tmpCap1.read()
        tmpCap2 = (cv2.VideoCapture("http://192.168.199.3:8765/picture/2/current/?_username=admin&_signature=8364b7955ab9bcfe1b2717c91ea1b2d6f2f59a6a"))
        found2, frame2 = tmpCap2.read()
        tmpFrames.append(frame1)
        tmpFrames.append(frame2)
        self.makeDirectory(len(self.caps))
        if(found1&found2):
            for frm in tmpFrames:
                if (self.saveInDirectory):
                    cv2.imwrite("./Pictures/Frame_" + str(count) + "/imageFrame_" + str(count) + "_" + str(
                        self.imageCount) + ".jpg", frm)
                else:
                    cv2.imwrite("./Pictures/imageFrame_" + str(count) + "_" + str(self.imageCount) + ".jpg", frm)
                count += 1
            print(str(count) + " picture(s) taken")
            self.imageCount += 1
        return

    def takePictureLocal(self):
        count = 0
        f = []
        f.clear()
        self.makeDirectory(len(self.caps))
        for c in self.caps:
            ret, frame = c.read()
            f.append(frame)

        for frm in f:
            if(self.saveInDirectory):
                cv2.imwrite("./Pictures/Frame_"+str(count)+"/imageFrame_" + str(count) + "_" + str(self.imageCount) + ".jpg", frm)
            else:
                cv2.imwrite("./Pictures/imageFrame_" + str(count) + "_" + str(self.imageCount) + ".jpg", frm)
            count += 1
        print(str(count)+" picture(s) taken")
        self.imageCount += 1
        return

    def deleteDirectory(self, frameCount):
        try:
            os.rmdir(os.getcwd() + "/Pictures/Frame_" + str(frameCount))
        except:
            print("Failed to delete folder")

    def makeDirectory(self, frameCount):
        if (os.path.exists(os.getcwd() + "/Pictures")&(self.saveInDirectory)):
            for i in range(0, frameCount):
                if not (os.path.exists(os.getcwd() + "/Pictures/Frame_" + str(i))):
                    os.mkdir(os.getcwd() + "/Pictures/Frame_" + str(i))
            return
        else:
            try:
                self.path = os.getcwd()
                self.path = self.path + "/Pictures"
                os.mkdir(self.path)
                if(self.saveInDirectory):
                    for i in range(0, frameCount):
                        os.mkdir(self.path + "/Frame_" + str(i))

            except OSError:
                print("Creation of the directory %s failed" % self.path)
            else:
                print("Successfully created the directory %s " % self.path)

    def lookForDevices(self, useWeb):
        portTestRange = 3
        count = 0
        start = -1
        if not useWeb:
            print("Looking for devices(local)")
            for i in range(start, portTestRange):
                cap = (cv2.VideoCapture(i, cv2.CAP_DSHOW))
                found, frame = cap.read()
                if (found):
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
                    cap = (cv2.VideoCapture("http://192.168.199.3:808"+str(i)+"/"))
                    timeDelta = (int(round(time.time())))-timestampStart
                    found, frame = cap.read()
                    if (found):
                        count += 1
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                        print("Device found on Port " + str(i))
                        self.caps.append(cap)
                else:
                    print("Could not find device(time exceeded)")
                    return count
        return count

    def endProgram(self):
        self.frames.clear()
        for c in self.caps:
            c.release()
        cv2.destroyAllWindows()
        print("Program stopped")
        os._exit(2)

    def __del__(self):
        self.frames.clear()
        for c in self.caps:
            c.release()
        cv2.destroyAllWindows()
        print("Program stopped")
        os._exit(1)





