import ImagingApi
import cv2

# if you are using a laptop just disable the web cam in your device-manager if you want to

cap = ImagingApi.CameraApi(640, 480, False, True)  # resolution(with, height), put Pictures in separate folder, use web or local device search

cap.keyListener()  # is needed for closing windows or making pictures

cap.makeVideo()
"""count = 0
while(True):
    tmpCap1 = (cv2.VideoCapture(
        "http://192.168.199.3:8765/picture/1/current/?_username=admin&_signature=405e3e47c0b54c48c7539decf8437b48bb320e16"))
    found1, frame1 = tmpCap1.read()
    tmpCap2 = (cv2.VideoCapture(
        "http://192.168.199.3:8765/picture/2/current/?_username=admin&_signature=8364b7955ab9bcfe1b2717c91ea1b2d6f2f59a6a"))
    found2, frame2 = tmpCap2.read()
    cv2.imshow("0", frame1)
    cv2.imshow("1", frame2)
    if(cv2.waitKey(1)==32):
        cv2.imwrite("Pictures/imageFrame_0_"+str(count)+".jpg", frame1);
        cv2.imwrite("Pictures/imageFrame_1_"+str(count)+".jpg", frame2)
        count = count + 1
        print("Image Taken: " + str(count))
"""