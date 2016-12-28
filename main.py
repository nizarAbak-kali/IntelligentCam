# coding: utf8

"""
https://intelligent-cam.firebaseio.com/
"""

import time

import cv2
from firebase import firebase

# si false plus de printing
DEBUG = True

# nom de la base de donné publique lié à l'application (à changé par votre propre bd)
fire = firebase.FirebaseApplication('https://intelligentcam-90d8f.firebaseio.com/', None)

# les xml de qui serve a la detection du visage ainsi que celle des yeux
cascadePath = "haarcascade_frontalface_default.xml"
eyes_cascadesPath = "haarcascade_eye.xml"


def get_time():
    if DEBUG: print("time !!")
    time_hhmmss = time.strftime('%H:%M:%S')
    date_ddmmyyyy = time.strftime('%m/%d/%Y')
    return time_hhmmss, date_ddmmyyyy


# pour lire la nouvelles entré dans la base (surtout pour les tests )
def get_data():
    if DEBUG: print("time !!")
    result = fire.get('/toto', None)
    print("get_data : " + str(result))


def send_data(i):
    time_hhmmss, date_ddmmyyyy = get_time()

    # data = str(i) + ',' + str(time_hhmmss) + ',' + str(date_ddmmyyyy)

    data = {'message': i, 'date': date_ddmmyyyy, 'time': time_hhmmss}

    res = fire.post('/toto', data)

    if DEBUG: print("send_data : " + str(res))


def detectface(image_capted):
    # creation du detecteur de visage
    faceCascade = cv2.CascadeClassifier(cascadePath)
    eye_cascade = cv2.CascadeClassifier(eyes_cascadesPath)
    # on enrengistre dans faces les differents visages
    faces = faceCascade.detectMultiScale(image_capted, scaleFactor=1.3, minNeighbors=5,
                                         minSize=(30, 30))
    # si  on veut sauvegarder la liste des boites couvrant les visages
    # rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in faces]

    #on boucle sur les boites couvrants les visages
    for (x, y, w, h) in faces:
        #dessin du contours
        cv2.rectangle(image_capted, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi = image_capted[y:y + h, x:x + w]
        # boucles sur les boites des yeux
        eyes = eye_cascade.detectMultiScale(roi)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    # pour affichage de l'images + dessins
    # if DEBUG : cv2.imshow('img', image_capted)
    # on attends a l'infinie (boucle infinie en quelque sortes)
    #if DEBUG : cv2.waitKey(20)

    # si visage detecter on retourne true
    if len(faces) != 0:
        return True
    return False


if __name__ == '__main__':
    i = "visage detecte !!"
    # capture de la video
    cap = cv2.VideoCapture(0)

    # Boucle infini

    while True:

        # capture image par image
        ret, im = cap.read()

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        if (detectface(gray)):
            try:
                send_data(i)

                if DEBUG: get_data()

            except IOError:
                print('Error! Something went wrong')
            print("face detected now entering sleep mode for 3 minutes")
            time.sleep(180)
