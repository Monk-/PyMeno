from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END, filedialog, simpledialog
import collections
import re
import os
import findMusicAlgorithm1 as algo
import databaseManagement as datMan

class GUI(Frame):
    def __init__(self, parent):
        """init"""
        Frame.__init__(self, parent)
        self.right_list = Listbox(parent)
        self.left_list = Listbox(parent)
        self.parent = parent
        self.initui()


    def initui(self):
        """getting all things started"""
        self.parent.title("PyMeno")
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=False)
        menu2_parse = Menu(menu_bar, tearoff=False)
        sub_menu = Menu(file_menu, tearoff=False)
        self.left_list.pack(side=LEFT, fill=BOTH, expand=2)
        self.right_list.pack(side=RIGHT, fill=BOTH, expand=2)

        #add something to menu

        #submenu.add_command(label="New feed")
        #submenu.add_command(label="Bookmarks")
        #submenu.add_command(label="Mail")
        #fileMenu.add_cascade(label='Import', menu=sub_menu, underline=0)

        file_menu.add_command(label="Choose folder with music", underline=0, command=self.openMen)
        file_menu.add_command(label="Exit", underline=0, command=self.onExit)

        menu2_parse.add_command(label="Download artists list", underline=0, command=datMan.download_list_of_artists)
        menu2_parse.add_command(label="Parse artists information to database", underline=0, command=self.show_entry)

        menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        menu_bar.add_cascade(label="Data", underline=0, menu=menu2_parse)

    def show_entry(self):
        try:
            number = int(simpledialog.askstring('Number', 'How many artists?'))
            print(number)
            datMan.parseFile(number)
        except:
            pass

    def onExit(self):
        self.quit()

    def openMen(self):
        dir_name = filedialog.askdirectory(parent=self, initialdir="/", title='Please select a directory')
        self.config(cursor="wait")
        self.update()
        for dir_path, dir_names, file_names in os.walk(dir_name):
            for filename in file_names:
                algo.changeTitle(self, os.path.join(dir_path, filename))
        self.config(cursor="")
            #self.sklearnBagOfWords()
               #print(self.list1)

    def insert_to_right_list_box(self, artist, song):
        self.right_list.insert(END, artist + " - " + song)