"""gui and gui methods"""
from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END, filedialog, simpledialog
import os
import find_music_algorithm as alMus
import webbrowser
import database_management as datMan



class GUI(Frame):
    """class for GUI"""
    def __init__(self, parent):
        """init"""
        Frame.__init__(self, parent)
        self.right_list = Listbox(parent)
        self.left_list = Listbox(parent)
        self.left_list.bind("<Double-Button-1>", on_double_click)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """getting all things started"""
        self.parent.title("PyMeno")
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=False)
        menu2_parse = Menu(menu_bar, tearoff=False)
        #menu3_parse = Menu(menu_bar, tearoff=False)
        # sub_menu = Menu(file_menu, tearoff=False)
        self.left_list.pack(side=LEFT, fill=BOTH, expand=2)
        self.right_list.pack(side=RIGHT, fill=BOTH, expand=2)

        # add something to menu

        # submenu.add_command(label="New feed")
        # submenu.add_command(label="Bookmarks")
        # submenu.add_command(label="Mail")
        # fileMenu.add_cascade(label='Import', menu=sub_menu, underline=0)

        file_menu.add_command(label="Choose folder with music ALG 2",
                              underline=0, command=self.open_menu)
        file_menu.add_command(label="Choose folder with music ALG 1",
                              underline=0, command=self.open_menu_ver_2)
        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)

        menu2_parse.add_command(label="Download artists list", underline=0,
                                command=datMan.download_list_of_artists)
        menu2_parse.\
            add_command(label="Parse artists information to database", underline=0,
                        command=go_to_lilis_parsing)
        menu2_parse.add_command(label="Show", underline=0, command=self.show_stats)
        menu2_parse.add_command(label="Show by album", underline=0,
                                command=self.show_stats_by_album)

        menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        menu_bar.add_cascade(label="Data", underline=0, menu=menu2_parse)

    def show_stats(self):
        """show stats in listbox"""
        datMan.get_music_stats(self)

    def show_stats_by_album(self):
        """show stats by album in listbox"""
        datMan.get_music_stats_by_album(self)

    def on_exit(self):
        """quit"""
        self.quit()

    def open_menu(self):
        """select directory with music, alg 1"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')
        self.config(cursor="wait")
        self.update()
        for data in os.walk(dir_name):
            for filename in data[2]:
                alMus.change_title(self, os.path.join(data[0], filename))
        self.config(cursor="")
        alMus.search_for_simmilar_ver_2(self)

    def open_menu_ver_2(self):
        """select directory with music, alg 2"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')
        self.config(cursor="wait")
        self.update()
        for data in os.walk(dir_name):
            for filename in data[2]:
                alMus.change_title(self, os.path.join(data[0], filename))
        self.config(cursor="")
        alMus.search_for_simmilar_ver_1(self)

    def insert_to_right_list_box(self, artist, song):
        """insert to right listbox for other methods"""
        self.right_list.insert(END, artist + " - " + song)

    def insert_to_left_list_box(self, artist):
        """insert to left listbox for other methods"""
        self.left_list.insert(END, artist)

def go_to_lilis_parsing():
    """how many artist do you want to parse"""
    number = int(simpledialog.askstring('Number', 'How many artists?'))
    print(number)
    datMan.parse_file_lil_version(number)

def on_double_click(event):
    """open youtube on double click"""
    new = 2  # open in a new tab, if possible
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    url = alMus.youtube_search(value)
    webbrowser.open(url, new=new)
