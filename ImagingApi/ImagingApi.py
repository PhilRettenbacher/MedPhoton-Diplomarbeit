import cv2;

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

    def writePicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        cv2.imwrite("image_1.jpg", frame)
        cv2.imwrite("image_2.jpg", frame2)

    def getPicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        return (frame, frame2)

    def showPicture(self):
        frame, frame2 = self.getPicture()

        cv2.imshow("Image1", frame)
        cv2.imshow("Image2", frame2)

        cv2.waitKey(3000)

    def videoStream(self):
        while (True):
            self.showPicture()
            if cv2.waitKey(1) == 27:
             break

    def __del__(self):
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()
