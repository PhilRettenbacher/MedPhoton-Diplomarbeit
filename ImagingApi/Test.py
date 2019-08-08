import ImagingApi

# if you are using a laptop just disable the web cam in your device-manager if you want to

cap = ImagingApi.CameraApi(640, 480, False, True)  # resolution(with, height), put Pictures in separate folder, use web or local device search

cap.keyListener()  # is needed for closing windows or making pictures

cap.makeVideo()

