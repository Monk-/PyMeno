from tkinter import Frame, Listbox, Menu, LEFT, RIGHT, BOTH, END
from tkinter import filedialog
import os
from PyLyrics import *
import urllib.request
import collections, re
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pickle

from mutagen.id3 import ID3


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.listbox1 = Listbox(parent)
        self.listbox = Listbox(parent)
        self.parent = parent
        self.initui()
        self.list = {}
        self.list1 = collections.Counter()
        self.list2 = []

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
            self.sklearnBagOfWords()
               #print(self.list1)

    def changeTitle(self, pathtofile):
        try:
            audio = ID3(pathtofile)
            self.listbox.insert(END, audio['TPE1'].text[0] + " - " + audio["TIT2"].text[0]) # ID3 - black magic of the unicorn
            try:
                self.list[audio['TPE1'].text[0]].append(audio["TIT2"].text[0])
                #self.addSongToList(audio['TPE1'].text[0],audio["TIT2"].text[0])
            except KeyError:
                self.list[audio['TPE1'].text[0]] = [audio["TIT2"].text[0]]
                #self.addSongToList(audio['TPE1'].text[0],audio["TIT2"].text[0])
            self.getBagOfWords(audio['TPE1'].text[0],audio["TIT2"].text[0])
        except:
            pass

    def download_list_of_artists(self):
        urllib.request.urlretrieve("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=d70d8067d56b2afc78942623d4256817&limit=1000", "scrobble.xml")

    def parseFile(self):
        tree = ET.parse('scrobble.xml')
        root = tree.getroot()
        list3 = []
        counter = 0
        for x in root.findall('.//name'):
            counter += 1
            print(x.text, counter)
            try:
                 for g in PyLyrics.getAlbums(x.text):
                    try:
                         for track in PyLyrics.getTracks(g):
                            try:
                                list3.append(PyLyrics.getLyrics(track.artist, track.name).lower())
                                print(track.artist, track.name)
                            except ValueError:
                                print(track.artist, track.name, " ERROR ")
                                pass
                    except:
                        print("MEGA ERROR")
                        pass
            except:
                print("GIGA ERROR")
        with open("pickle200.p", 'wb') as f:
            pickle.dump(list3, f)

    def tokeni(self,data):
        return [SnowballStemmer("english").stem(word) for word in data.split()]

    def preprocessor(self, data):
        return " ".join([SnowballStemmer("english").stem(word) for word in  data.split()])

    def getBagOfWords(self, artistName, songName):
        song = PyLyrics.getLyrics(artistName, songName).lower().split()
        song = [word for word in song if word not in stop_words.get_stop_words('english')]
        song = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in song]
        p = collections.Counter(song)
        self.list1 = self.list1 + p

    def addSongToList(self, artistName, songName):
        self.list2.append(PyLyrics.getLyrics(artistName, songName).lower())



    def sklearnBagOfWords(self):
        vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
        bagOfWords = vectorizer.fit(self.list2)
        bagOfWords = vectorizer.transform(self.list2)
        #with open("pickle.p", 'wb') as f:
            #pickle.dump(bagOfWords, f)
        #bagOfWords1 = pickle.load(open("pickle.p","rb"))
        #print(bagOfWords1)
        self.hhh()

    def hhh(self):
        vectorizer3 = CountVectorizer(stop_words=stopwords.words('english'))
        bagOfWords3 = vectorizer3.fit(self.list2)
        bagOfWords3 = vectorizer3.fit_transform(self.list2)
        print(bagOfWords3.toarray()[0])
        bagOfWords1 = pickle.load(open("pickle.p","rb"))
        vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
        bagOfWords = vectorizer.fit(bagOfWords1)
        bagOfWords = vectorizer.transform(bagOfWords1)
        neigh = NearestNeighbors()
        neigh.fit(bagOfWords.toarray())
        print(bagOfWords.shape)
        print(bagOfWords3.shape)
        print(neigh.kneighbors(bagOfWords3.toarray()))
        print(neigh.n_neighbors)

