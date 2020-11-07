import numpy as np
import cv2 as cv
import time

api = "rtsp://192.168.2.202:554/MainStream"
webcam = 0

cap = cv.VideoCapture(webcam)
time.sleep(2.0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("[INFO] Type incomming to processing frame :" + str(type(frame)))

    # Our operations on the frame come here
    # rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
