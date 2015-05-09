#!/usr/bin/python
# -*- coding: utf-8 -*-

from guiclass import Example
from tkinter import *
from PyLyrics import *

def createGui():
    root = Tk()
    root.geometry("800x400+300+300")
    app = Example(root)
    root.mainloop()


#a = PyLyrics.getLyrics("3 D","Duck and run")
#print(a) #Print the lyrics directly
createGui()
