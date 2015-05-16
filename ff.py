#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *

from PyLyrics import *
import pickle
from guiclass import Example
from gui import GUI

def createGui():
    root = Tk()
    root.geometry("800x400+300+300")
    app = GUI(root)
    root.mainloop()

createGui()

