import ImagingApi

# if you are on a laptop just disable the web cam if you want to

cap = ImagingApi.CameraApi(640,480,False, False) #resolution(with, height), put Pictures in separate folder, use web or local device search

cap.keyListener()
cap.makeVideo()



