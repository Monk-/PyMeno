from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import *
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
import math
import gui as gui
import random
from tkinter import END

# Important to not put the same values into users library again
List_artists_songs = []
# kind of temporary
Catalog = Counter()
# Dict of words per artist
my_bag = {}
# Dict of songs per artist
# Its have to be that way because user doesnt has to have all album
my_bag_c = {}
# Dict of words per library
my_bag_all = Counter()
# There we have a dict of average of word per song for each artist
Average_of_word_per_song_per_author = {}
# There we have a dict of average of word per song for all music user's library
Average_of_word_per_song = 0
# MIN and MAX average of word per song
__min__ = 0
__max__ = 0


def change_title(self, path_to_file):
    """
    This function takes out information about author and title of songs from file
    """
    try:
        audio = ID3(path_to_file)
        # Checking if filed was already parsed
        if str(audio['TPE1'].text[0] + "," + audio["TIT2"].text[0]) not in List_artists_songs:
            self.insert_to_right_list_box(audio['TPE1'].text[0], audio["TIT2"].text[0])
            bag_of_words(audio['TPE1'].text[0], audio["TIT2"].text[0])
            List_artists_songs.append(str(audio['TPE1'].text[0] + "," + audio["TIT2"].text[0]))
        else:
            # If was
            print("That was already parsed", " : \n", audio['TPE1'].text[0], "::", audio["TIT2"].text[0])
    except ValueError:
        pass


def bag_of_words(artist_name, song_name):
    """
    Simple bag of words
    We used here a lemmatize to simplify form of words for example running -> run
    And stopwords to remove them from dict
    """
    global my_bag_all
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
        # When we parse new artist we catch the except KeyError and put new key into dict
        print("Parsing author : ", artist_name, " : Please wait... : )")
        my_bag[artist_name] = cnt
        my_bag_c[artist_name] = 1
    for v in my_bag.values():
        my_bag_all += v


def search_for_simmilar_ver_2(self):
    """
    # Algorithm II #
    We parts our code to have more visibility of what we doing
    There is algorithm which at the beginning catch
    the number of intersections between dicts then use cosine similarity
    """
    made_group_smaller()
    first_step()
    temp = second_step()
    temp = fourth_step(temp)
    temp = fifth_step(temp)
    six_step(self, temp)


def search_for_simmilar_ver_1(self):
    """
    # Algorithm I #
    This algorithm based mainly on cosine similarity
    """
    made_group_smaller()
    first_step()
    temp = another_try()
    temp = fourth_step(temp)
    temp = fifth_step(temp)
    six_step(self, temp)


def made_group_smaller():
    """
    This function is calculating an average of
    words per author and defining max and min
    """
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


def first_step():
    """
    This function loads a date from pickle and put them into dict
    """
    global Catalog
    data2 = dict(pickle.load(open("pickleLilEvery.p", 'rb')))
    Catalog.clear()
    Catalog.update({k: v for k, v in data2.items()})


def second_step():
    """
    This function is defining dictionary of songs with dictionary
    based on amount of shared most popular words in users libraries
    """
    shared_items = {}
    data2 = dict(pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb')))
    # Here we are making an intersections between
    # all popular words in our library and each song in library of comparing songs
    for k, v in Catalog.items():
        shared_items[k] = len(set(Counter(v)) & set(my_bag_all))
    # There we choose only authors with average of word per song between max and min of our music library
    kk = Counter({k: v for k, v in shared_items.items() if(__max__ >= data2[k] >= __min__) is True}).most_common(15)
    b, c = zip(*sorted(kk, key=lambda d: d[1], reverse=True))
    return b


def another_try():
    """
    This function is another option of comparing, this time is depend on cosine similarity.
    The purpose is to find the perfect artist
    """
    shared_items = {}
    data2 = dict(pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb')))
    for k, v in Catalog.items():
        shared_items[k] = counter_cosine_similarity(Counter(v), my_bag_all)
    print(shared_items)
    kk = Counter({k: v for k, v in shared_items.items() if(__max__ >= data2[k] >= __min__) is True}).most_common(15)
    b, c = zip(*sorted(kk, key=lambda d: d[1], reverse=True))
    return b


def fourth_step(list_chosen):
    """
    This function make another comparing, this time is depend on cosine similarity.
    The purpose is to find the perfect album from chosen artist
    """
    shared_items_add = {}
    data2 = pickle.load(open("pickleLil300.p", 'rb'))
    data2.update(pickle.load(open("pickleLil500.p", 'rb')))
    data2.update(pickle.load(open("pickleLil303.p", 'rb')))
    # We need to pick up some date from pickle with dicts of words from each album of artist
    for k, v in data2.items():
        temp = k.split(',', 1)
        if temp[0] in list_chosen:
            shared_items_add[k] = counter_cosine_similarity(Counter(v), my_bag_all)
    # In shared_items[artist,album} we have value of similarity
    temp = Counter({k: v for k, v in shared_items_add.items() if v not in my_bag_all.keys()})
    print(temp)
    b, c = zip(*sorted(temp.most_common(20), key=lambda d: d[0]))
    return b


def fifth_step(b):
    """
    This function is randomly choosing a song from chosen album
    """
    shared_items_add = {}
    print("Suggest : ")
    for k in b:
        temp = k.split(',', 1)
        albums = PyLyrics.getAlbums(singer=temp[0])
        for x in albums:
            if x.name == temp[1]:
                tracks = x.tracks()
                num = random.randint(0, len([track.name for track in tracks])-1)
                print(temp[0], ":", tracks[num].name)
                shared_items_add[k] = tracks[num].name
    return shared_items_add


def six_step(self, shared_items_add):
    """
    This function display chosen titles on GUI
    """
    self.left_list.delete(0, END)
    for k, v in shared_items_add.items():
        temp = k.split(',', 1)
        gui.GUI.insert_to_left_list_box(self, temp[0] + " : " + v)


def counter_cosine_similarity(v1, v2):
    """
    This function calculate similarity between vector
    the closer to 1 the more similar are the songs
    """
    # a * b = ||a|| ||b|| cos(theta)
    terms = set(v1).union(v2)
    # A * B
    dot_product = sum(v1.get(k, 0) * v2.get(k, 0) for k in terms)
    # || A ||
    magnitude_a = math.sqrt(sum(v1.get(k, 0)**2 for k in terms))
    # || B ||
    magnitude_b = math.sqrt(sum(v2.get(k, 0)**2 for k in terms))
    return dot_product / (magnitude_a * magnitude_b)