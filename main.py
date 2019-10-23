import os
import sys
import cv2 as cv
import numpy as np
from getFrame import GetFrame
from processFrame import ProcessFrame
from dotenv import load_dotenv


# Initializing main code
load_dotenv(verbose=True)

print("[INFO] We are running on ==> " + os.name)

FPS = int(os.getenv("FPS"))
DNN = os.getenv("DNN")


class MainApp():

    def __init__(self):
        # Initialize GetFrame Class etc ...
        self.gettingFrame = GetFrame()
        self.currentFrame = None
        self.frameCount = 0
        self.api_modeFirst = os.getenv("API_MODE1")
        self.api_modeSecond = os.getenv("API_MODE2")

        # init ProcessFrame Class
        self.processingThread = ProcessFrame(DNN, self.api_modeSecond)
        if self.api_modeFirst == "USB":
            self.initialize_main("API_USB", self.api_modeFirst)

        else:
            self.initialize_main("API_IP_CAMERA", self.api_modeFirst)


    def initialize_main(self, api_cam_init, api_modeFirst_init):
        self.api = os.getenv(api_cam_init)
        print("[INFO] Using IP CAMERA: " + self.api)
        # init get frame
        try:
            self.gettingFrame.open_camera(self.api, api_modeFirst_init)
        except ValueError:
            print(ValueError.__str__())
            print("[INFO] Exiting program...")
            sys.exit()


    def mainLoop(self):
        while True:

            # get frame
            self.currentFrame = self.gettingFrame.get_frame()

            if self.currentFrame[1] is not None:

                # increment frame count
                self.frameCount += 1

                if (self.frameCount > FPS) and (self.currentFrame[0] == True):
                    self.processingThread.start(self.currentFrame[1])
                    self.frameCount = 0
                else:
                    continue


main = MainApp()
main.mainLoop()