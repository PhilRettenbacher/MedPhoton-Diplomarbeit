import cv2
import os
from pynput.keyboard import Key, Listener, Controller, KeyCode

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

        self.__del__()

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
        portTestRange = 10
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
            portTestRange = 3
            start = 1
            print("Looking for devices(web)")
            for i in range(start, portTestRange):
                cap = (cv2.VideoCapture("http://192.168.199.3:808"+str(i)+"/"))
                found, frame = cap.read()
                if (found):
                    count += 1
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    print("Device found on Port " + str(i))
                    self.caps.append(cap)
        return count

    def __del__(self):
        self.frames.clear()
        for c in self.caps:
            c.release()
        cv2.destroyAllWindows()
        print("Program stopped")


    # def __init__(self, useWeb, id):
    #
    #     self.useWeb = useWeb
    #     self.id = id
    #
    #     self.init()
    #
    # def init(self):
    #     if(self.useWeb):
    #         print("Initialize Camera in Web ...");
    #         self.cap1 = cv2.VideoCapture('http://192.168.199.3:808' + str(self.id[0]) + '/')
    #         self.cap2 = cv2.VideoCapture('http://192.168.199.3:808' + str(self.id[1]) + '/')
    #         if(not self.cap1.isOpened() or not self.cap2.isOpened()):
    #             print("Cameras could not be initialized!");
    #             self.enabled = False
    #             return
    #     else:
    #         print("Initialize Camera locally ...");
    #         self.cap1 = cv2.VideoCapture(self.id[0], cv2.CAP_DSHOW);
    #         self.cap2 = cv2.VideoCapture(self.id[1], cv2.CAP_DSHOW);
    #         if(not self.cap1.isOpened() or not self.cap2.isOpened()):
    #             print("Cameras could not be initialized!");
    #             self.enabled = False
    #             return
    #     self.enabled = True
    #
    # def checkEnabled(self):
    #     if not self.enabled:
    #         print("Cameras are not enabled/working/attached")
    #         exit(1)
    # def readCameras(self):
    #     self.checkEnabled()
    #
    #
    #
    # def writePicture(self):
    #     if not self.checkEnabled():
    #         return
    #
    #     ret, frame = self.cap1.read()
    #     ret2, frame2 = self.cap2.read()
    #
    #     cv2.imwrite("image_1.jpg", frame)
    #     cv2.imwrite("image_2.jpg", frame2)
    #
    # def getPicture(self):
    #     if not self.checkEnabled():
    #         return
    #
    #     ret, frame = self.cap1.read()
    #     ret2, frame2 = self.cap2.read()
    #
    #     return (frame, frame2)
    #
    # def showPicture(self, waitTime):
    #     if not self.checkEnabled():
    #         return
    #
    #     frame, frame2 = self.getPicture()
    #
    #     cv2.imshow("Image1", frame)
    #     cv2.imshow("Image2", frame2)
    #
    #     cv2.waitKey(waitTime)
    #
    # def videoStream(self):
    #     if not self.checkEnabled():
    #         return
    #
    #     while (True):
    #         self.showPicture(1)
    #         if cv2.waitKey(1) == 27:
    #          break
    #
    # def __del__(self):
    #     self.cap1.release()
    #     self.cap2.release()
    #     cv2.destroyAllWindows()
    #
    # def setActive(self,id,enabled):
    #     try:
    #         if enabled:
    #             with urllib.request.urlopen('http://192.168.199.3:7999/' + str(id) + '/action/restart') as response:
    #                 html = response.read()
    #         else:
    #             with urllib.request.urlopen('http://192.168.199.3:7999/' + str(id) + '/action/quit') as response:
    #                 html = response.read()
    #     except:
    #         TRED = '\033[31m'
    #         print(TRED + "Website can't be reached!")
    #     else:
    #         TGREEN = '\033[32m'
    #         print(TGREEN + "Camera restarted/quitted")
    #     self.init()
    #
    # def restartCams(self):
    #     self.setActive(1, True)
    #     self.setActive(2, True)
    #
    # def quitCams(self):
    #     self.setActive(1, False)
    #     self.setActive(2, False)
    #
    # def rebootCams(self):
    #     self.quitCams()
    #     time.sleep(5)
    #     self.restartCams()



