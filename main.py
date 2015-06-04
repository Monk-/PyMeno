#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from gui import GUI


def create_gui():
    root = Tk()
    root.geometry("800x400+300+300")
    GUI(root)
    root.mainloop()

create_gui()
