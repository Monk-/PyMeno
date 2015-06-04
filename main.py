"""main class"""
from tkinter import Tk
from gui import GUI


def create_gui():
    """create gui"""
    root = Tk()
    root.geometry("800x400+300+300")
    GUI(root)
    root.mainloop()

create_gui()
