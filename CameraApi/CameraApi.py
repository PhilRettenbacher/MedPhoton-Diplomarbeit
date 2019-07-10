import cv2;

class CameraApi:
    def __init__(self, useWeb, id):

        if(useWeb):
            print("Initialize Camera in Web");
        else:
            print("Initialize Camera locally");
            self.cap1 = cv2.VideoCapture(id[0], cv2.CAP_DSHOW);
            self.cap2 = cv2.VideoCapture(id[1], cv2.CAP_DSHOW);


    def writePicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        cv2.imwrite("image_1.jpg", frame)
        cv2.imwrite("image_2.jpg", frame2)

    def getPicture(self):
        ret, frame = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        return (frame, frame2)
