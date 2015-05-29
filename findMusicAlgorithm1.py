from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import *
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
import math

bag = Counter()
Catalog = Counter()
my_bag = {}
my_bag_c = {}
my_bag_all = Counter()
Average_of_word_per_song_per_author = {}
Average_of_word_per_song = 0
__min__ = 0
__max__ = 0
key_idx = {}


def change_title(self, path_to_file):
    try:
        audio = ID3(path_to_file)
        self.insert_to_right_list_box(audio['TPE1'].text[0], audio["TIT2"].text[0])
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
    except KeyError:
        print("Parsing author : ", artist_name, " : Please wait... : )")
        my_bag[artist_name] = cnt
        my_bag_c[artist_name] = 1
    # bag.update(Counter({k: v for k, v in cnt.items() if v > 2}))


def made_group_smaller():
    global __max__
    global __min__
    for x in sorted(list(my_bag), key=lambda s: s.lower()):
        Average_of_word_per_song_per_author[x] = len(my_bag[x])/my_bag_c[x]
        print(x, " : Average of words per author : ", len(my_bag[x])/my_bag_c[x])
    print(dict(my_bag_c))
    __max__ = max(Average_of_word_per_song_per_author.values())
    print("MAX", str(__max__))
    __min__ = min(Average_of_word_per_song_per_author.values())
    print("MIN", str(__min__))
    first_step()


def first_step():
    # Defining dictionary of songs based on amount of words per song
    data2 = dict(pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb')))
    Catalog.update(Counter({k: v for k, v in data2.items()}))
    # max__ >= v >= __min__}))
    second_step()


def second_step():
    # Defining dictionary of songs with dictionary of the most popular words per artist
    global Catalog
    data2 = dict(pickle.load(open("pickleLilEvery.p", 'rb')))
    data2.update({k: v for k, v in data2.items()})
    ff = {k: v for k, v in data2.items() if k in Catalog.keys()}
    Catalog.clear()
    Catalog.update(Counter(ff))
    third_step()


def third_step():
    global my_bag_all
    # Defining dictionary of songs with dictionary based on amount of shared most popular words in users libraries
    global my_bag_all
    data2 = dict(pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb')))
    shared_items = {}
    shared_items_add = {}
    for v in my_bag.values():
        my_bag_all += v
    # print(Catalog.items())
    for k, v in Catalog.items():
        # print(Counter(v).items())
        # print(my_bag_all.items())
        shared_items[k] = len(set(Counter(v)) & set(my_bag_all))
    # print(shared_items)

    # my personal method
    for v in sorted(shared_items, key=shared_items.get, reverse=True):
        print(v, shared_items[v])
    ff = Counter()
    ff.update(Counter({k: v for k, v in shared_items.items() if __max__ >= data2[k] >= __min__}))
    print(ff)
    # counter_cosine_similarity
    for k, v in Catalog.items():
        shared_items_add[k] = counter_cosine_similarity(Counter(v), my_bag_all)
    print(shared_items_add)
    for v in sorted(shared_items_add, key=shared_items_add.get, reverse=True):
        if v not in my_bag_all.keys():
            print(v, shared_items_add[v])


def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)
