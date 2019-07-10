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

    def __del__(self):
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()