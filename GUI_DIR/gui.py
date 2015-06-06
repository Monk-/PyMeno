"""gui and gui methods"""

from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END, filedialog, simpledialog
from tkinter import ttk
import os
import webbrowser
import argparse
from googleapiclient.discovery import build


class GUI(Frame):  # pylint: disable=too-many-ancestors
    """class for GUI"""

    def __init__(self, parent, db, pab, alg):
        """init"""
        Frame.__init__(self, parent)
        self.right_list = Listbox(parent)
        self.left_list = Listbox(parent)
        self.left_list.bind("<Double-Button-1>", self.on_double_click)
        self.parent = parent
        self.db_creator = db
        self.path_and_bag = pab
        self.alg_do = alg
        self.queue = queue.Queue()
        self.init_ui()

    def init_ui(self):
        """getting all things started"""
        self.parent.title("PyMeno")
        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=False)
        menu2_parse = Menu(menu_bar, tearoff=False)
        # menu3_parse = Menu(menu_bar, tearoff=False)
        # sub_menu = Menu(file_menu, tearoff=False)
        self.left_list.pack(side=LEFT, fill=BOTH, expand=2)
        self.right_list.pack(side=RIGHT, fill=BOTH, expand=2)

        # add something to menu

        file_menu.add_command(label="Choose folder with music ALG 1",
                              underline=0, command=self.new_thread_2)
        file_menu.add_command(label="Choose folder with music ALG 2",
                              underline=0, command=self.open_menu)
        file_menu.add_command(label="Choose folder with music ALG 3",
                              underline=0, command=self.open_menu_ver_3)
        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)

        menu2_parse.add_command(label="Download artists list", underline=0,
                                command=self.db_creator.download_list_of_artists)
        menu2_parse.\
            add_command(label="Parse artists information to database", underline=0,
                        command=self.go_to_lilis_parsing)


        menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        menu_bar.add_cascade(label="Data", underline=0, menu=menu2_parse)
        """sub_menu = Menu(menu_bar, tearoff=False)
        sub_menu.add_command(label="Video")
        sub_menu.add_command(label="Channel")
        sub_menu.add_command(label="Playlist")
        menu2_parse.add_cascade(label='Youtube search', menu=sub_menu, underline=0)"""

    def on_exit(self):
        """quit"""
        self.quit()

    def open_menu(self):
        """select directory with music, alg 1"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')
        self.config(cursor="wait")
        self.update()
        list_of_songs = []
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
        self.config(cursor="")
        shared_items_add = self.alg_do.search_for_simmilar_ver_2()
        self.left_list.delete(0, END)
        self.right_list.delete(0, END)
        for song in list_of_songs:
            temp = song.split(',', 1)
            self.insert_to_right_list_box(temp[0], temp[1])
        for key, value in shared_items_add.items():
            temp = key.split(',', 1)
            self.queue.put(temp[0] + " : " + value)
            self.insert_to_left_list_box(temp[0] + " : " + value)

    def new_thread_2(self):
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')

        if dir_name != "":
            self.path_and_bag.check_if_refresh(dir_name)
            self.config(cursor="wait")
            self.update()
            self.clean_queue()
            self.queue.put("Finding files in chosen folder:\n\n")
            num_files = len([val for sub_list in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(dir_name)] for val in sub_list])
            rott = tk.Tk()
            app = App(rott, self.queue, num_files)
            rott.protocol("WM_DELETE_WINDOW", app.on_closing)
            threading.Thread(target=self.open_menu_ver_2, args=(dir_name,)).start()
            app.mainloop()
        else:
            print("Action aborted")

    def clean_queue(self):
        if not self.queue.empty():
            while not self.queue.empty():
                self.queue.get()

    def open_menu_ver_2(self, dir_name):
        """select directory with music, alg 2"""
        list_of_songs = []
        self.path_and_bag.clear_bag_of_words()
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
                self.queue.put(filename)
        self.queue.put("\nAnd what we have here?:\n")
        self.config(cursor="")
        shared_items_add = self.alg_do.search_for_simmilar_ver_1(self.queue)
        self.left_list.delete(0, END)
        self.right_list.delete(0, END)
        for song in list_of_songs:
            temp = song.split(',', 1)
            self.insert_to_right_list_box(temp[0], temp[1])
        for key, value in shared_items_add.items():
            temp = key.split(',', 1)
            self.insert_to_left_list_box(temp[0] + " : " + value)
        self.queue.put("endino-tarantino")

    def open_menu_ver_3(self):
        """select directory with music, alg 3"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')
        list_of_songs = []
        self.config(cursor="wait")
        self.update()
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
        self.config(cursor="")
        shared_items_add = self.alg_do.search_for_simmilar_ver_3()
        self.left_list.delete(0, END)
        self.right_list.delete(0, END)
        for song in list_of_songs:
            temp = song.split(',', 1)
            self.insert_to_right_list_box(temp[0], temp[1])
        for key, value in shared_items_add.items():
            temp = key.split(',', 1)
            self.insert_to_left_list_box(temp[0] + " : " + value)

    def insert_to_right_list_box(self, artist, song):
        """insert to right listbox for other methods"""
        self.right_list.insert(END, artist + " - " + song)

    def insert_to_left_list_box(self, artist):
        """insert to left listbox for other methods"""
        self.left_list.insert(END, artist)

    def go_to_lilis_parsing(self):
        """how many artist do you want to parse"""
        number = int(simpledialog.askstring('Number', 'How many artists?'))
        print(number)
        self.db_creator.parse_file_lil_version(number)

    def on_double_click(self, event):
        """open youtube on double click"""
        new = 2  # open in a new tab, if possible
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        url = self.youtube_search(value)
        webbrowser.open(url, new=new)

    def run(self, number):
        try:
            app = App(self.queue, number)
            app.mainloop()
        except:
            print("ps")

    @staticmethod
    def youtube_search(to_search):
        """
            This function finds url to our songs throw Youtube API
        """
        # YouTube API
        developer_key = "AIzaSyCn9Pk4vWC8LjjIKqol5gkku20DI0IRurU"
        youtube_api_service_name = "youtube"
        youtube_api_version = "v3"
        parse = argparse.ArgumentParser()
        parse.add_argument("--q", help="Search term", default=to_search)
        parse.add_argument("--max-results", help="Max results", default=25)
        args = parse.parse_args()
        youtube = build(youtube_api_service_name, youtube_api_version, developerKey=developer_key)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(q=args.q,
                                                part="id,snippet",
                                                maxResults=args.max_results,
                                                order="viewCount").execute()

        videos = []
        channels = []
        play_lists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and play lists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(search_result["id"]["videoId"])
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                             search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
                play_lists.append("%s (%s)" % (search_result["snippet"]["title"],
                                               search_result["id"]["playlistId"]))

        try:
            return "https://www.youtube.com/watch?v=" + videos[0]
        except (UnicodeEncodeError, IndexError) as evil:
            return "https://www.youtube.com/watch?v=" + "_NXrTujMP50"


import tkinter as tk
import threading
import queue


class App(Frame):

    def __init__(self, master, queue1, number):
        Frame.__init__(self,master)
        self.root = master
        self.root.title("Please, bear with me, for a moment : )")
        self.queue = queue1
        self.number = number
        self.listbox = tk.Listbox(self.root, width=50, height=20)
        self.progressbar = ttk.Progressbar(self.root, orient='horizontal',
                                           length=400, mode='determinate')
        self.listbox.pack(padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=10)
        self.listbox.delete(0, END)
        self.running = 1
        self._job = 0
        self.periodiccall()

    def periodiccall(self):
        self.checkqueue()
        if self.running:
            self._job = self.after(100, self.periodiccall)
        else:
            self.after_cancel(self._job)
            self._job = None
            self.root.destroy()
            self.root.quit()
            print("ASas")

    def on_closing(self):
        self.listbox.destroy()
        self.progressbar.destroy()
        self.root.destroy()
        self.root.quit()
        self.after_cancel(self._job)
        self._job = None

    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.listbox.insert('end', msg)
                self.listbox.yview(END)
                self.progressbar.step(100/(self.number + 30))
                if msg == "endino-tarantino":#crazy name so noone will ever have file named like this
                    self.running = 0
            except queue.Empty:
                #killing thread
                self.running = 0
                self.root.destroy()


