from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import *

bag = Counter()

def changeTitle(self, path_to_file):
    try:
        audio = ID3(path_to_file)
        self.insert_to_right_list_box(audio['TPE1'].text[0], audio["TIT2"].text[0])# ID3 - black magic of the unicorn
       # try:
       #     list[audio['TPE1'].text[0]].append(audio["TIT2"].text[0])
       # except KeyError:
       #     list[audio['TPE1'].text[0]] = [audio["TIT2"].text[0]]
        bag_of_words(audio['TPE1'].text[0], audio["TIT2"].text[0])
    except:
        pass


def bag_of_words(artist_name, song_name):
    global bag
    song = PyLyrics.getLyrics(artist_name, song_name).lower().split()
    song = [word for word in song if word not in stopwords.words('english')]
    song = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in song]
    cnt = Counter(song)
    bag.update(Counter({k:v for k, v in cnt.items() if v > 10}))

def extend_stop_words_list():
    pass
