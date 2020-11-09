# import numpy as np
import cv2 as cv
import time

__default_width__ = 640
__default_height__ = 480

api = "rtsp://10.42.0.204:5544/MainStream"
webcam = 0

cap = cv.VideoCapture(webcam)
time.sleep(2.0)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print("Frame Width  {}".format(width))
print("Frame height {}".format(height))


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("[INFO] Type incoming to processing frame {}" .format(frame))

    # Our operations on the frame come here
    # rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame = cv.resize(frame, (__default_width__, __default_height__))

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
