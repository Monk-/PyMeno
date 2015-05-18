from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import *
from nltk.stem.wordnet import WordNetLemmatizer
import gui as gui

bag = Counter()
my_bag = {}
my_bag_c = {}


def change_title(self, path_to_file):
    try:
        audio = ID3(path_to_file)
        self.insert_to_right_list_box(audio['TPE1'].text[0], audio["TIT2"].text[0])
        # ID3 - black magic of the unicorn
        # try:
        #     list[audio['TPE1'].text[0]].append(audio["TIT2"].text[0])
        # except KeyError:
        #     list[audio['TPE1'].text[0]] = [audio["TIT2"].text[0]]
        bag_of_words(self, audio['TPE1'].text[0], audio["TIT2"].text[0])
    except ValueError:
        pass


def bag_of_words(self, artist_name, song_name):
    global bag
    to_simpler_form = WordNetLemmatizer()
    song = PyLyrics.getLyrics(artist_name, song_name).lower().split()
    song = [word for word in song if word not in stopwords.words('english')]
    song = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in song]
    song = [to_simpler_form.lemmatize(x, 'v') for x in song]
    cnt = Counter(song)
    try:
        my_bag[artist_name] = my_bag[artist_name] + cnt
        my_bag_c[artist_name] += 1
    except:
        print("Parsing author : ", artist_name, " : Please wait... : )")
        my_bag[artist_name] = cnt
        my_bag_c[artist_name] = 1
    bag.update(Counter({k: v for k, v in cnt.items() if v > 2}))
    # print(my_bag, my_bag_c, bag)


def extend_stop_words_list():
    pass


def made_group_smaller():
    list_of = ()
    for x in sorted(list(my_bag), key=lambda s: s.lower()):
        print(x, " : Average of words per author : ", len(my_bag[x])/my_bag_c[x])