import cv2;
import numpy as np;
#The onboard webcam usually has the id 0
webcamID = 1;

cap = cv2.VideoCapture(webcamID, cv2.CAP_DSHOW);

counter = 0;

alpha = 3
beta = -150

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.convertScaleAbs(frame, frame, alpha, beta);

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) == 32:
        print("Image taken")
        cv2.imwrite("image_"+str(counter)+".jpg", frame);
        counter = counter + 1;

    if cv2.waitKey(1) == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()