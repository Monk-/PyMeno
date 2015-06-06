"""main class"""
from tkinter import Tk

from GUI_DIR.gui import GUI
from CORE.creatin_database import CreatingDatabase
from CORE.algh import FindMusic
from CORE.check_paths import MakeBagOfWords


class PyGame(object):

    def __init__(self):
        """create gui"""
        root = Tk()
        root.geometry("800x400+300+300")
        db = CreatingDatabase()
        check = MakeBagOfWords()
        alg = FindMusic(check.MY_BAG, check.MY_BAG_C)

        GUI(root, db, check, alg)
        root.mainloop()

PyGame()
