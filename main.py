import os
import sys
import cv2 as cv
import numpy as np
from getFrame import GetFrame
from processFrame import ProcessFrame
from dotenv import load_dotenv

load_dotenv(verbose=True)
frameCount = 0

print("[INFO] We are running on " + os.name)

api_modeFirst = os.getenv("API_MODE1")
api_modeSecond = os.getenv("API_MODE2")

if api_modeFirst == "USB":
    api = os.getenv("API_USB")
    print("[INFO] Using USB MODE: " + api)
    # init get frame
    try:
        gettingFrame = GetFrame(api, api_modeFirst)
    except ValueError:
        print(ValueError.__str__())
        print("[INFO] Exiting program...")
        sys.exit()

else:
    api = os.getenv("API_IP_CAMERA")
    print("[INFO] Using IP CAMERA: " + api)
    # init get frame
    try:
        gettingFrame = GetFrame(api, api_modeFirst)
    except ValueError:
        print(ValueError.__str__())
        print("[INFO] Exiting program...")
        sys.exit()

FPS = int(os.getenv("FPS"))
DNN = os.getenv("DNN")


# init process frame
processingThread = ProcessFrame(DNN, api_modeSecond)

while True:

    # get frame
    currentFrame = gettingFrame.get_frame()

    if currentFrame[1] is not None:

        #print("[INFO] Current frame = " + str(frameCount))
        # increment frame count
        frameCount += 1

        if (frameCount > FPS) and (currentFrame[0] == True):
            processingThread.start(currentFrame[1])
            frameCount = 0
        else:
            continue
