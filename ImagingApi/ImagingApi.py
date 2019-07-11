import cv2;
import urllib.request;

class CameraApi:
    def __init__(self, useWeb, id):

        self.useWeb = useWeb
        self.id = id

        self.init()



    def init(self):
        if(self.useWeb):
            print("Initialize Camera in Web");
            self.cap1 = cv2.VideoCapture('http://192.168.199.3:808' + str(self.id[0]) + '/')
            self.cap2 = cv2.VideoCapture('http://192.168.199.3:808' + str(self.id[1]) + '/')
        else:
            print("Initialize Camera locally");
            self.cap1 = cv2.VideoCapture(self.id[0], cv2.CAP_DSHOW);
            self.cap2 = cv2.VideoCapture(self.id[1], cv2.CAP_DSHOW);
            if(not self.cap1.isOpened() or not self.cap2.isOpened()):
                print("Cameras could not be initialized!");
                self.enabled = False
                return
        self.enabled = True
        
    def checkEnabled(self):
        if not self.enabled:
            print("Cameras are not enabled/working/attached")
        return self.enabled
    def writePicture(self):
        if not self.checkEnabled():
            return

        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        cv2.imwrite("image_1.jpg", frame)
        cv2.imwrite("image_2.jpg", frame2)

    def getPicture(self):
        if not self.checkEnabled():
            return

        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        return (frame, frame2)

    def showPicture(self, waitTime):
        if not self.checkEnabled():
            return

        frame, frame2 = self.getPicture()

        cv2.imshow("Image1", frame)
        cv2.imshow("Image2", frame2)

        cv2.waitKey(waitTime)

    def videoStream(self):
        if not self.checkEnabled():
            return

        while (True):
            self.showPicture(1)
            if cv2.waitKey(1) == 27:
             break

    def __del__(self):
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()

    def setActive(self,id,enabled):
        try:
            if enabled:
                print("Try to restart cam ...")
                with urllib.request.urlopen('http://192.168.199.3:7999/' + str(id) + '/action/restart') as response:
                    html = response.read()
            else:
                print("Try to quit cam ...")
                with urllib.request.urlopen('http://192.168.199.3:7999/' + str(id) + '/action/quit') as response:
                    html = response.read()
        except:
            TRED = '\033[31m'
            print(TRED + "Website can't be reached!")
        else:
            TGREEN = '\033[32m'
            print(TGREEN + "Success!!")
        self.init()

    def getBrightness(self):
        print ("test")
        return



