import cv2 as cv

class GetFrame:

    def __init__(self, video_source):

        self.vid = cv.VideoCapture(video_source, cv.CAP_FFMPEG)
        
        if not self.vid.isOpened():
            raise ValueError("[INFO] Unable to open camera ", video_source)
        
        # get cap property 
        self.width   = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)    # float
        self.height  = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)   # float

        print("[INFO] Width = " + str(self.width))
        print("[INFO] Height = " + str(self.height))


    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            #frame = cv.resize(frame, (self.width, self.height))
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)



    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
