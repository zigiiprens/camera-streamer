import cv2 as cv


class GetFrame:

    def __init__(self):
        print("[INFO] Initializing GetFrame Class")
        self.width = None
        self.height = None
        self.vid = None

    def open_camera(self, video_source, api_mode):
        if api_mode == "IP_CAMERA":
            self.vid = cv.VideoCapture(video_source, cv.CAP_FFMPEG)
        elif api_mode == "WEBCAM":
            self.vid = cv.VideoCapture(int(video_source))

        if not self.vid.isOpened():
            raise ValueError("[INFO] Unable to open camera ", video_source)

        # get cap property 
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)  # float
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)  # float

        print("[INFO] Width = " + str(self.width))
        print("[INFO] Height = " + str(self.height))

    def get_frame(self, ret=None):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv.resize(frame, (int(0.4 * self.width), int(0.5 * self.height)))
            if ret:
                return ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
