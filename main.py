import cv2
cap = cv2.VideoCapture('http://192.168.43.81:8081/')
cap2 = cv2.VideoCapture('http://192.168.43.81:8082/')

while True:
  ret, frame = cap.read()
  ret2, frame2 = cap2.read()

  cv2.namedWindow("Video")
  cv2.imshow('Video', frame)
  cv2.namedWindow("Video2")
  cv2.imshow("Video2", frame2)

  if cv2.waitKey(1) == 27:
    exit(0)