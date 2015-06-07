"""main class"""
from tkinter import Tk

from gui_dir import GUI
from core import MakeBagOfWords, FindMusic, CreatingDatabase


class PyMeno(object):
    """runs app"""
    def __init__(self):
        """create gui"""
        self.root = Tk()
        self.root.geometry("800x400+300+300")
        self.db_parser = CreatingDatabase()
        self.check = MakeBagOfWords()
        self.alg = FindMusic(self.check.my_bag, self.check.my_bag_c)
        self.say_credit()
        self.run_app()

    def run_app(self):
        """run method"""
        GUI(self.root, self.db_parser, self.check, self.alg)
        self.root.mainloop()

    @staticmethod
    def say_credit():
        """credits"""
        print("Authors:")
        print("Klaudia Olejniczak")
        print("Oleksandr Kuzhel")

PyMeno()
