import os
import cv2 as cv
import numpy as np
from threading import Thread


class ProcessFrame():

    def __init__(self, algorithm):

        self.imgDataFolder = "data/img/"
        self._count = 0
        self.confidence_threshold = 0.5
        self.process_frame = None
        self.stopped = False

        if algorithm == "CAFFE":
            self.modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
            self.configFile = "models/deploy.prototxt"
            self.net = cv.dnn.readNetFromCaffe(self.configFile, self.modelFile)
            print("[INFO] Loaded model from CAFFE")
        else:
            self.modelFile = "models/opencv_face_detector_uint8.pb"
            self.configFile = "models/opencv_face_detector.pbtxt"
            self.net = cv.dnn.readNetFromTensorflow(
                self.modelFile, self.configFile)
            print("[INFO] Loaded model from TENSORFLOW")

    def start(self, frame):
        try:
            self.process_frame = frame
        except:
            print("[INFO] Could not copy frame into process_frame")

        Thread(target=self.processDetect, args=()).start()

    def processDetect(self):
        #print("[INFO] Starting thread")
        while not self.stopped:
            self.process_frame = self.process_frame[:, :, ::-1]
            (h, w) = self.process_frame.shape[:2]
            blob = cv.dnn.blobFromImage(cv.resize(
                self.process_frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

            self.net.setInput(blob)
            self.detections = self.net.forward()

            if self.process_frame is not None:

                #print("[INFO] Process_frame is ready for detections")
                # loop over the detections
                for i in range(0, self.detections.shape[2]):
                    # extract the confidence (i.e., probability) associated with the
                    # prediction
                    self.confidence = self.detections[0, 0, i, 2]
                    # filter out weak detections by ensuring the `confidence` is
                    if self.confidence < self.confidence_threshold:
                        continue
                    self.box = self.detections[0, 0,
                                               i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = self.box.astype("int")
                    #face_locations += [(startY, endX, endY, startX)]
                    self.cropped_frame = self.process_frame[startY:endY, startX:endX]
                    self.write_string = self.imgDataFolder + \
                        str(self._count) + ".jpg"
                    cv.imwrite(self.write_string, self.cropped_frame)
                    print("[INFO] Found faces, saving face to " +
                          self.write_string)
                    self._count += 1
            else:
                print("[INFO] Process_frame is empty")

            #self.confidence = 0
            self.stopped = True
            #print("[INFO] Stopping thread")

        self.stopped = False

    def stop(self):
        self.stopped = True
