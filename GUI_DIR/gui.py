"""gui and gui methods"""
import tkinter as tk
from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END, filedialog, simpledialog
from tkinter import ttk
import os
import webbrowser
import argparse
from googleapiclient.discovery import build
import threading
import queue
import logging


class GUI(Frame):  # pylint: disable=too-many-ancestors
    """class for GUI"""
    static_logger = logging.getLogger(__name__)
    static_queue = queue.Queue()

    def __init__(self, parent, db, pab, alg):
        """init"""
        Frame.__init__(self, parent)
        self.right_list = Listbox(parent)
        self.left_list = Listbox(parent)
        self.parent = parent
        self.db_creator = db
        self.path_and_bag = pab
        self.alg_do = alg
        self.menu_bar = Menu(self.parent)
        self.init_ui()

    def init_ui(self):
        """getting all things started"""
        self.parent.title("PyMeno")
        self.left_list.bind("<Double-Button-1>", self.on_double_click)
        self.parent.config(menu=self.menu_bar)
        file_menu = Menu(self.menu_bar, tearoff=False)
        menu2_parse = Menu(self.menu_bar, tearoff=False)
        # menu3_parse = Menu(menu_bar, tearoff=False)
        # sub_menu = Menu(file_menu, tearoff=False)
        self.left_list.pack(side=LEFT, fill=BOTH, expand=2)
        self.right_list.pack(side=RIGHT, fill=BOTH, expand=2)

        # add something to menu

        file_menu.add_command(label="Choose folder with music ALG 1",
                              underline=0, command=self.new_thread_2)
        file_menu.add_command(label="Choose folder with music ALG 2",
                              underline=0, command=self.new_thread_1)
        file_menu.add_command(label="Choose folder with music ALG 3",
                              underline=0, command=self.new_thread_2)
        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)

        menu2_parse.add_command(label="Download artists list", underline=0,
                                command=self.db_creator.download_list_of_artists)
        menu2_parse.\
            add_command(label="Parse artists information to database", underline=0,
                        command=self.go_to_lilis_parsing)

        self.menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        self.menu_bar.add_cascade(label="Data", underline=0, menu=menu2_parse)

    def on_exit(self):
        """quit"""
        GUI.static_queue.put("endino-tarantino")
        self.quit()

    def disable_menu(self):
        """disable menu while program is working"""
        self.menu_bar.entryconfig("File", state="disabled")
        self.menu_bar.entryconfig("Data", state="disabled")

    def enable_menu(self):
        """enable menu after work"""
        self.menu_bar.entryconfig("File", state="normal")
        self.menu_bar.entryconfig("Data", state="normal")

    def new_thread_1(self):
        """thread for the first algorythm"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')

        if dir_name != "":
            self.disable_menu()
            self.path_and_bag.check_if_refresh(dir_name)
            self.config(cursor="wait")
            self.update()
            self.clean_queue()
            GUI.static_queue.put("Finding files in chosen folder:\n\n")
            num_files = len([val for sub_list in
                             [[os.path.join(i[0], j)for j in i[2]]
                              for i in os.walk(dir_name)]
                             for val in sub_list])
            rott = tk.Tk()
            app = App(rott, GUI.static_queue, num_files)
            rott.protocol("WM_DELETE_WINDOW", app.on_closing)
            thread = threading.Thread(target=self.open_menu, args=(dir_name,))
            thread.setDaemon(True)
            thread.start()
            app.mainloop()
        else:
            print("Action aborted")

    def open_menu(self, dir_name):
        """select directory with music, alg 1"""
        list_of_songs = []
        self.path_and_bag.clear_bag_of_words()
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
                GUI.static_queue.put(filename)
        if not list_of_songs:
            print("action aborted")
        else:
            GUI.static_queue.put("\nAnd what we have here?:\n")
            self.config(cursor="")
            shared_items_add = self.alg_do.search_for_simmilar_ver_2(False, GUI.static_queue)
            if not shared_items_add:
                shared_items_add = self.alg_do.search_for_simmilar_ver_2(True, GUI.static_queue)
            if shared_items_add:
                self.left_list.delete(0, END)
                self.right_list.delete(0, END)
                for song in list_of_songs:
                    temp = song.split(',', 1)
                    self.insert_to_right_list_box(temp[0], temp[1])
                for key, value in shared_items_add.items():
                    temp = key.split(',', 1)
                    GUI.static_queue.put(temp[0] + " : " + value)
                    self.insert_to_left_list_box(temp[0] + " : " + value)
        GUI.static_queue.put("endino-tarantino")
        self.enable_menu()

    def new_thread_2(self):
        """thread for the second algorythm"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')

        if dir_name != "":
            self.disable_menu()
            self.path_and_bag.check_if_refresh(dir_name)
            self.config(cursor="wait")
            self.update()
            self.clean_queue()
            GUI.static_queue.put("Finding files in chosen folder:\n\n")
            num_files = len([val for sub_list in
                             [[os.path.join(i[0], j)for j in i[2]]
                              for i in os.walk(dir_name)]
                             for val in sub_list])
            rott = tk.Tk()
            app = App(rott, GUI.static_queue, num_files)
            rott.protocol("WM_DELETE_WINDOW", app.on_closing)
            thread = threading.Thread(target=self.open_menu_ver_2, args=(dir_name,))
            thread.setDaemon(True)
            thread.start()
            app.mainloop()
        else:
            print("Action aborted")

    @staticmethod
    def clean_queue():
        """cleaning queue if user exit manualy"""
        if not GUI.static_queue.empty():
            while not GUI.static_queue.empty():
                GUI.static_queue.get()

    def open_menu_ver_2(self, dir_name):
        """select directory with music, alg 2"""
        list_of_songs = []
        self.path_and_bag.clear_bag_of_words()
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
                GUI.static_queue.put(filename)
        if not list_of_songs:
            print("action aborted")
        else:
            GUI.static_queue.put("\nAnd what we have here?:\n")
            self.config(cursor="")
            shared_items_add = self.alg_do.search_for_simmilar_ver_1(False, GUI.static_queue)
            if not shared_items_add:
                shared_items_add = self.alg_do.search_for_simmilar_ver_1(True, GUI.static_queue)
            if shared_items_add:
                self.left_list.delete(0, END)
                self.right_list.delete(0, END)
                for song in list_of_songs:
                    temp = song.split(',', 1)
                    self.insert_to_right_list_box(temp[0], temp[1])
                for key, value in shared_items_add.items():
                    temp = key.split(',', 1)
                    self.insert_to_left_list_box(temp[0] + " : " + value)
        GUI.static_queue.put("endino-tarantino")
        self.enable_menu()

    def new_thread_3(self):
        """thread for the third algorythm"""
        dir_name = filedialog.askdirectory(parent=self, initialdir="/",
                                           title='Please select a directory')

        if dir_name != "":
            self.disable_menu()
            self.path_and_bag.check_if_refresh(dir_name)
            self.config(cursor="wait")
            self.update()
            self.clean_queue()
            GUI.static_queue.put("Finding files in chosen folder:\n\n")
            num_files = len([val for sub_list in
                             [[os.path.join(i[0], j)
                               for j in i[2]] for i in os.walk(dir_name)]
                             for val in sub_list])
            rott = tk.Tk()
            app = App(rott, GUI.static_queue, num_files)
            rott.protocol("WM_DELETE_WINDOW", app.on_closing)
            thread = threading.Thread(target=self.open_menu_ver_3, args=(dir_name,))
            thread.setDaemon(True)
            thread.start()
            app.mainloop()
        else:
            print("Action aborted")

    def open_menu_ver_3(self, dir_name):
        """select directory with music, alg 3"""

        list_of_songs = []
        self.path_and_bag.clear_bag_of_words()
        for data in os.walk(dir_name):
            for filename in data[2]:
                list_of_songs = self.path_and_bag.change_title(os.path.join(data[0], filename))
                GUI.static_queue.put(filename)
        print(list_of_songs)
        if not list_of_songs:
            print("action aborted")
        else:
            GUI.static_queue.put("\nAnd what we have here?:\n")
            self.config(cursor="")
            shared_items_add = self.alg_do.search_for_simmilar_ver_3(False, GUI.static_queue)
            if not shared_items_add:
                shared_items_add = self.alg_do.search_for_simmilar_ver_3(True, GUI.static_queue)
            if shared_items_add:
                self.left_list.delete(0, END)
                self.right_list.delete(0, END)
                for song in list_of_songs:
                    temp = song.split(',', 1)
                    self.insert_to_right_list_box(temp[0], temp[1])
                for key, value in shared_items_add.items():
                    temp = key.split(',', 1)
                    self.insert_to_left_list_box(temp[0] + " : " + value)
        GUI.static_queue.put("endino-tarantino")
        self.enable_menu()

    def insert_to_right_list_box(self, artist, song):
        """insert to right listbox for other methods"""
        self.right_list.insert(END, artist + " - " + song)

    def insert_to_left_list_box(self, artist):
        """insert to left listbox for other methods"""
        self.left_list.insert(END, artist)

    def go_to_lilis_parsing(self):
        """how many artist do you want to parse"""
        number_from = simpledialog.askstring('Number', 'How many artists?/FROM')
        if number_from is not None:
            number_from = int(number_from)
        print(number_from)
        number_to = int(simpledialog.askstring('Number', 'How many artists?/TO'))
        if number_to is not None:
            number_to = int(number_to)
        print(number_to)
        self.db_creator.parse_file(number_to, number_from)

    def on_double_click(self, event):
        """open youtube on double click"""
        new = 2  # open in a new tab, if possible
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        url = self.youtube_search(value)
        webbrowser.open(url, new=new)

    @staticmethod
    def youtube_search(to_search):
        """
            This function finds url to our songs throw Youtube API
        """
        developer_key = "AIzaSyCn9Pk4vWC8LjjIKqol5gkku20DI0IRurU"
        youtube_api_service_name = "youtube"
        youtube_api_version = "v3"
        parse = argparse.ArgumentParser()
        parse.add_argument("--q", help="Search term", default=to_search)
        parse.add_argument("--max-results", help="Max results", default=25)
        args = parse.parse_args()
        youtube = build(youtube_api_service_name,
                        youtube_api_version, developerKey=developer_key)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(q=args.q,  # pylint: disable=no-member
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
        except (UnicodeEncodeError, IndexError):
            GUI.static_logger.error('ERROR', exc_info=True)
            return "https://www.youtube.com/watch?v=" + "_NXrTujMP50"


class App(Frame):  # pylint: disable=too-many-ancestors
    """information window class"""
    static_running = 1
    static_job = 0

    def __init__(self, master, queue1, number):
        """initialising view"""
        Frame.__init__(self, master)
        self.root = master
        self.root.title("Please, bear with me, for a moment : )")
        GUI.static_queue = queue1
        self.number = number
        self.logger = logging.getLogger(__name__)
        self.listbox = tk.Listbox(self.root, width=65, height=20)
        self.progressbar = ttk.Progressbar(self.root, orient='horizontal',
                                           length=400, mode='determinate')
        self.listbox.pack(padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=10)
        self.listbox.delete(0, END)
        App.static_running = 1
        App.static_job = 0
        self.periodiccall()

    def periodiccall(self):
        """function called periodical to get new information"""
        self.check_queue()
        if App.static_running:
            App.static_job = self.after(100, self.periodiccall)
        else:
            self.after_cancel(App.static_job)
            App.static_job = None
            self.root.destroy()
            self.root.quit()
            print("helping window is closing")

    def on_closing(self):
        """override what to do on manual close"""
        self.listbox.destroy()
        self.progressbar.destroy()
        self.root.destroy()
        self.root.quit()
        self.after_cancel(App.static_job)
        App.static_job = None

    def check_queue(self):
        """check queue"""
        while GUI.static_queue.qsize():
            try:
                msg = GUI.static_queue.get(0)
                self.listbox.insert('end', msg)
                self.listbox.yview(END)
                self.progressbar.step(100/(self.number + 30))
                if msg == "endino-tarantino":  # crazy name so noone will ever have file like this
                    App.static_running = 0
            except queue.Empty:
                # killing thread
                self.logger.error('ERROR', exc_info=True)
                App.static_running = 0
                self.root.destroy()
