from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END, filedialog, simpledialog
import collections
import re
import os
import findMusicAlgorithm1 as alMus
import databaseManagement as datMan


class GUI(Frame):
    """class for GUI"""
    def __init__(self, parent):
        """init"""
        Frame.__init__(self, parent)
        self.right_list = Listbox(parent)
        self.left_list = Listbox(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """getting all things started"""
        self.parent.title("PyMeno")
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=False)
        menu2_parse = Menu(menu_bar, tearoff=False)
        menu3_parse = Menu(menu_bar, tearoff=False)
        # sub_menu = Menu(file_menu, tearoff=False)
        self.left_list.pack(side=LEFT, fill=BOTH, expand=2)
        self.right_list.pack(side=RIGHT, fill=BOTH, expand=2)

        # add something to menu

        # submenu.add_command(label="New feed")
        # submenu.add_command(label="Bookmarks")
        # submenu.add_command(label="Mail")
        # fileMenu.add_cascade(label='Import', menu=sub_menu, underline=0)

        file_menu.add_command(label="Choose folder with music", underline=0, command=self.open_menu)
        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)

        menu2_parse.add_command(label="Download artists list", underline=0, command=datMan.download_list_of_artists)
        menu2_parse.add_command(label="Parse artists information to database", underline=0, command=self.show_entry)

        menu3_parse.\
            add_command(label="Parse artists information to database", underline=0, command=self.go_to_lilis_parsing)
        menu3_parse.add_command(label="Show", underline=0, command=self.show_stats)
        menu3_parse.add_command(label="Show by album", underline=0, command=self.show_stats_by_album)

        menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        menu_bar.add_cascade(label="Data", underline=0, menu=menu2_parse)
        menu_bar.add_cascade(label="Lily options", underline=0, menu=menu3_parse)

    def show_entry(self):
        try:
            number = int(simpledialog.askstring('Number', 'How many artists?'))
            print(number)
            datMan.parseFile(number)
        except IOError:
            pass

    def show_stats(self):
        datMan.get_music_stats(self)

    def show_stats_by_album(self):
        datMan.get_music_stats_by_album(self)

    def go_to_lilis_parsing(self):
        number = int(simpledialog.askstring('Number', 'How many artists?'))
        print(number)
        datMan.parse_file_lil_version(number)

    def on_exit(self):
        self.quit()

    def open_menu(self):
        dir_name = filedialog.askdirectory(parent=self, initialdir="/", title='Please select a directory')
        self.config(cursor="wait")
        self.update()
        for dir_path, dir_names, file_names in os.walk(dir_name):
            for filename in file_names:
                alMus.change_title(self, os.path.join(dir_path, filename))
        self.config(cursor="")
        alMus.search_for_simmilar(self)

    def insert_to_right_list_box(self, artist, song):
        self.right_list.insert(END, artist + " - " + song)

    def insert_to_left_list_box(self, artist):
        self.left_list.insert(END, artist)