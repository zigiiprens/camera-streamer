import os
import sys
import cv2 as cv
import numpy as np
from getFrame import GetFrame
from processFrame import ProcessFrame

frameCount = 0

# global variables
api = "rtsp://192.168.2.202:554/MainStream"     # IP Camera, can use 0 for default
DNN = "CAFFE"                                   # Face detect model used


# init get frame
try:
    gettingFrame = GetFrame(api)
except ValueError:
    print(ValueError.__str__())
    print("[INFO] Exiting program...")
    sys.exit()


# init process frame
processingThread = ProcessFrame(DNN)


while True:

    # get frame
    currentFrame = gettingFrame.get_frame()

    if currentFrame[1] is not None:

        #print("[INFO] Current frame = " + str(frameCount))
        # increment frame count
        frameCount += 1

        if (frameCount > 30) and (currentFrame[0] == True):
            processingThread.start(currentFrame[1])
            frameCount = 0
        else:
            continue

    #print("[INFO] Alive thread count : " + "unknown")

    # showing the frame
    #cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break
