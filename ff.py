#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *

from PyLyrics import *
import nltk
from guiclass import Example


def createGui():
    root = Tk()
    root.geometry("800x400+300+300")
    app = Example(root)
    #app.downloadFile()
   # app.parseFile()

    root.mainloop()


#a = PyLyrics.getLyrics("3 D","Duck and run")
#print(a) #Print the lyrics directly
createGui()

