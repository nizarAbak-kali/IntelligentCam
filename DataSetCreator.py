import os

import cv2
import numpy as np
from PIL import Image

import FaceDBSQlite
import UserModel

DEBUG = True


class DataSetCreator:
    def __init__(self, path='dataSet'):
        self.path_Dataset = path
        self.imagePaths = [os.path.join(self.path_Dataset, f) for f in os.listdir(self.path_Dataset)]

    def getImagesWithID(self):
        faces = []
        IDs = []
        for imagePath in self.imagePaths:
            faceImg = Image.open(imagePath).convert('L');
            faceNP = np.array(faceImg, "uint8");
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNP)
            IDs.append(ID)
            if DEBUG:
                cv2.imshow("trainnig", faceNP)
                cv2.waitKey(10)
        return np.array(IDs), faces

    def addUsers(self):
        face_Cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        db = FaceDBSQlite.DBlite3("test.db")

        cam = cv2.VideoCapture(0)
        id = input("id ? : ")
        name = input("name ? : ")
        i = 10
        while i >= 0:
            ret, cap = cam.read()
            gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
            faces = face_Cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
                                                  minSize=(30, 30))

            for (x, y, w, h) in faces:
                # dessin du contours
                roi = gray[y:y + h, x:x + w]
                cv2.imwrite(name + str(id) + ".jpg", roi)
                f = open(name + str(id) + ".jpg", 'rb')
                img = f.read()
                u = UserModel.UserModel(id, name, img)
                db.add(u)
            i -= 1
        db.saveDB()
