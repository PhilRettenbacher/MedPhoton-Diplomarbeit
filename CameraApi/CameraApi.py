import cv2;

class CameraApi:
    def __init__(self, useWeb, id):

        if(useWeb):
            print("Initialize Camera in Web");
        else:
            print("Initialize Camera locally");
            self.cap1 = cv2.VideoCapture(id[0], cv2.CAP_DSHOW);
            self.cap2 = cv2.VideoCapture(id[1], cv2.CAP_DSHOW);

