import os
import sys
from getFrame import GetFrame
from processFrame import ProcessFrame
from dotenv import load_dotenv

# Initializing main code
load_dotenv(verbose=True)

print("[INFO] System architecture is {}" .format(sys.platform()))

__fps__ = int(os.getenv("FPS"))
__dnn__ = os.getenv("DNN")


class MainApp:
    def __init__(self):
        # Initialize GetFrame Class etc ...
        self.gettingFrame = GetFrame()
        self.currentFrame = None
        self.frameCount = 0
        self.url = None
        self.api_modeFirst = os.getenv("API_MODE1")
        self.api_modeSecond = os.getenv("API_MODE2")

        # init ProcessFrame Class
        self.processingThread = ProcessFrame(__dnn__, self.api_modeSecond)
        if self.api_modeFirst == "WEBCAM":
            self.initialize_main("API_WEBCAM", self.api_modeFirst)
        else:
            self.initialize_main("API_IP_CAMERA", self.api_modeFirst)

    def initialize_main(self, api_cam_init, api_mode_first_init):
        self.url = os.getenv(api_cam_init)
        print("[INFO] Using IP CAMERA link: {}" .format(self.url))
        # init get frame
        try:
            self.gettingFrame.open_camera(self.url, api_mode_first_init)
        except ValueError:
            print(ValueError.message)
            print("[INFO] Exiting program...")
            sys.exit()

    def main_loop(self):
        while True:
            # get frame
            self.currentFrame = self.gettingFrame.get_frame()

            if self.currentFrame[1] is not None:
                # increment frame count
                self.frameCount += 1

                if self.frameCount > __fps__:
                    if self.currentFrame[0]:
                        self.processingThread.start(self.currentFrame[1])
                        self.frameCount = 0
                else:
                    continue


if __name__ == '__main__':
    main = MainApp()
    main.main_loop()
