# import numpy as np
import cv2 as cv
import time

__default_width__ = 1920
__default_height__ = 1080

api = "rtsp://admin:@10.42.0.204:5544/MainStream"
gst = ('rtspsrc location={} latency={} ! application/x-rtp, payload=96, encoding-name=H264 !'
		'rtpjitterbuffer mode=1 ! rtph264depay !'
               	' h264parse ! nvv4l2decoder ! nvvidconv! video/x-raw, format=BGRx !'
               	' videoconvert ! video/x-raw, format=BGR ! appsink ').format(api, 0)
webcam = 0

cap = cv.VideoCapture(gst, cv.CAP_GSTREAMER)
# cap = cv.VideoCapture(api)
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
