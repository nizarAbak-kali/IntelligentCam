#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3 as lite


class DBlite3:
    def __init__(self, name):
        self.con = lite.connect(name)
        self.cursor = self.con.cursor()
        if (not os.path.isfile('user.sql')):
            print("found previous db trying to load it")
            self.loadDB()
            print("load finished")

    def createTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS Users")
        self.cursor.execute("CREATE TABLE Users(UserId INT, Name TEXT, Image BLOB)")
        self.con.commit(0)

    def add(self, user):
        id, name, img = user.getUser()
        binary = lite.Binary(img)

        obj = (id, name, binary)
        self.cursor.execute("INSERT INTO Users VALUES(?,?,?)", obj)
        self.con.commit()

    def getUserById(self, id):
        self.cursor.execute("SELECT * FROM Users WHERE UserID=" + str(id))
        rows = self.cursor.fetchone()
        return rows

    def saveDB(self):
        f = open('user.sql', 'w')
        data = '\n'.join(self.con.iterdump())
        with f:
            f.write(data)

    def loadDB(self):
        f = open('user.sql', 'r')
        with f:
            data = f.read()
            self.cursor.executescript(data)
            self.con.commit()
