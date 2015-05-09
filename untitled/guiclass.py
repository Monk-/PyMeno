from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END
from tkinter import filedialog
import os
import re
from mutagen.id3 import ID3

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.listbox1 = Listbox(parent)
        self.listbox = Listbox(parent)
        self.parent = parent
        self.initui()

    def initui(self):

        self.parent.title("Submenu")

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=False)

        submenu = Menu(fileMenu, tearoff=False)

        self.listbox.pack(side=LEFT, fill=BOTH, expand=2)
        # listbox.insert(END, "a list entry")

       # self.listbox1 = Listbox(self.parent)
        self.listbox1.pack(side=RIGHT, fill=BOTH, expand=2)

        #listbox1.insert(END, "a sssslist entry")
       # submenu.add_command(label="New feed")
        #submenu.add_command(label="Bookmarks")
        #submenu.add_command(label="Mail")
        #fileMenu.add_cascade(label='Import', menu=submenu, underline=0)

       # fileMenu.add_separator()

        fileMenu.add_command(label="Choose folder with music", underline=0, command=self.openMen)
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)


    def onExit(self):
        self.quit()

    def openMen(self):
        dirname = filedialog.askdirectory(parent=self, initialdir="/", title='Please select a directory')
        for dirpath, dirnames, filenames in os.walk(dirname):
            for filename in filenames:
                self.changeTitle(os.path.join(dirpath, filename))

    def changeTitle(self, pathtofile):
        try:
            audio = ID3(pathtofile)
            self.listbox.insert(END, audio['TPE1'].text[0] + " - " + audio["TIT2"].text[0]) # ID3 - black magic of the unicorn
        except:
            pass

