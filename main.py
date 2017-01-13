# coding: utf8

"""
https://intelligent-cam.firebaseio.com/
"""

import time

import cv2

from FaceDetector import FaceDetector
from FirebaseClass import FirebaseClass

time_beetween_detection = 180

if __name__ == '__main__':
    i = "visage detecte !!"
    # capture de la video
    cap = cv2.VideoCapture(0)

    firebaseclass = FirebaseClass('https://intelligentcam-90d8f.firebaseio.com/', '/toto')
    facedetector = FaceDetector("haarcascade_frontalface_default.xml")


    # Boucle infini
    while True:
        ret, im = cap.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if (facedetector.detectface(gray)):
            try:
                # bool, ids = facedetector.recognizeface()

                # for id in ids:
                #    firebaseclass.send_data(id, gray)
                firebaseclass.send_data(i, gray)
            except IOError:
                print('Error! Something went wrong')
            print("face detected now entering sleep mode for 3 minutes")
            time.sleep(time_beetween_detection)
