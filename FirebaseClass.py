import time

import cv2
import numpy
from firebase import firebase

DEBUG = False


class FirebaseClass:
    def __init__(self, link_to_fireApp, node):
        self.fire = firebase.FirebaseApplication(link_to_fireApp, None)
        self.time_hhmmss = ""
        self.date_ddmmyyyy = ""
        self.child_node = node  # par ex '/toto'

    def get_time(self):
        if DEBUG: print("time !!")
        self.time_hhmmss = time.strftime('%H:%M:%S')
        self.date_ddmmyyyy = time.strftime('%m/%d/%Y')

    def get_data(self):
        if DEBUG: print("time !!")
        result = self.fire.get('/toto', None)
        if (DEBUG): print("get_data : " + str(result))

    def send_data(self, message, img):
        self.get_time()
        cv2.imwrite('tmp.jpg', img)
        data_t = cv2.imread('tmp.jpg')

        data = {'message': message, 'date': self.date_ddmmyyyy, 'time': self.time_hhmmss,
                'image': numpy.array_str(data_t)}
        # data = json.dumps(data)
        self.fire.post('/toto', data)
        if DEBUG: print("send_data")
