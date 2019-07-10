import cv2;
import urllib.request;

class CameraApi:
    def __init__(self, useWeb, id):

        if(useWeb):
            print("Initialize Camera in Web");
            self.cap1 = cv2.VideoCapture('http://192.168.199.3:808' + str(id[0]) + '/')
            self.cap2 = cv2.VideoCapture('http://192.168.199.3:808' + str(id[1]) + '/')
        else:
            print("Initialize Camera locally");
            self.cap1 = cv2.VideoCapture(id[0], cv2.CAP_DSHOW);
            self.cap2 = cv2.VideoCapture(id[1], cv2.CAP_DSHOW);
            if(not self.cap1.isOpened() or not self.cap2.isOpened()):
                print("Cameras could not be initialized!");
                exit(0)

    def writePicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        cv2.imwrite("image_1.jpg", frame)
        cv2.imwrite("image_2.jpg", frame2)

    def getPicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        return (frame, frame2)

    def showPicture(self, waitTime):
        frame, frame2 = self.getPicture()

        cv2.imshow("Image1", frame)
        cv2.imshow("Image2", frame2)

        cv2.waitKey(waitTime)

    def videoStream(self):
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
            TGREEN = '\033[31m'
            print(TGREEN + "Website can't be reached!")
        else:
            TGREEN = '\033[32m'
            print(TGREEN + "Success!!")

