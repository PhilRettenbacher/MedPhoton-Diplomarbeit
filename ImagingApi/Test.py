import ImagingApi

cap = ImagingApi.CameraApi(640,480,True, False) #resolution(with, height), put Pictures in separate folder, use web or local device search

cap.keyListener()

cap.makeVideo()


