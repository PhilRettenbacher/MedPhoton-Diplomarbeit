from ImagingApi import ImagingApi

cam = ImagingApi.CameraApi(True, (1,2))

cam.videoStream()
cam.setActive(2, True)





