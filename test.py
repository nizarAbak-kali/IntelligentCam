#!/usr/bin/python
# -*- coding: utf-8 -*-

import DataSetCreator
import FaceDBSQlite
import UserModel


def readImage(path):
    try:
        fin = open(path, "rb")
        img = fin.read()
        return img

    except IOError as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))


    finally:

        if fin:
            fin.close()


u1 = UserModel.UserModel(0, "roro", readImage("tmp.jpg"))
u2 = UserModel.UserModel(2, "toto", readImage("tmp.jpg"))
u3 = UserModel.UserModel(4, "totf", readImage("tmp.jpg"))

db = FaceDBSQlite.DBlite3("test.db")

db.add(u1)
db.add(u2)
db.add(u3)
db.saveDB()
rows = db.getUserById(4)
print(rows)

Dataset = DataSetCreator.DataSetCreator()
Dataset.addUsers()
