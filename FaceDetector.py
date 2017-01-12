import cv2

import DataSetCreator
from  DataSetCreator import DataSetCreator

DEBUG = True


class FaceDetector:
    def __init__(self, path_face):
        self.face_Cascade = cv2.CascadeClassifier(path_face)
        # self.eye_Cascade = cv2.CascadeClassifier(path_eyes)
        self.face_detected = []
        # self.recognizer = cv2.createLBPHFaceRecognizer()

    def detectface(self, image_capted):
        # on enrengistre dans faces les differents visages
        faces = self.face_Cascade.detectMultiScale(image_capted, scaleFactor=1.3, minNeighbors=5,
                                                   minSize=(30, 30))
        # si  on veut sauvegarder la liste des boites couvrant les visages
        # rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in faces]

        # on boucle sur les boites couvrants les visages
        for (x, y, w, h) in faces:
            # dessin du contours
            cv2.rectangle(image_capted, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = image_capted[y:y + h, x:x + w]
            self.face_detected.append(roi)
            # boucles sur les boites des yeux
        #   eyes = self.eye_Cascade.detectMultiScale(roi)
        #  for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        # pour affichage de l'images + dessins
        if DEBUG: cv2.imshow('img', image_capted)
        # on attends a l'infinie (boucle infinie en quelque sortes)
        if DEBUG: cv2.waitKey(20)

        # si visage detecter on retourne true
        if len(faces) != 0:
            return True
        return False

    def train_recon(self, faces, Ids):
        data = DataSetCreator.DataSetCreator()
        i, j = data.getImagesWithID()

        # self.recognizer.train(faces,np.array(Ids))
        # self.recognizer.save('recognizer/trainingData.yml')
        return

    def load(self):
        self.recognizer.load('recognizer/trainingData.yml')

    def recognizeface(self):
        ids = []
        confs = []
        for i in self.face_detected:
            id, conf = self.recognizer.predict(i)
            ids.append(id)
            confs.append(conf)
        if len(ids) != 0:
            return True, ids
        return False, ids
