"""
    In this file we have function to split lyrics of songs with user's library
    into dicts and looks for other similarly songs
"""
from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import PyLyrics
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
import math
import gui as gui
import random
from tkinter import END

# Important to not put the same values into users library again
LIST_ARTIST_SONGS = []
# kind of temporary
CATALOG = Counter()
# Dict of words per artist
MY_BAG = {}
# Dict of songs per artist
# Its have to be that way because user doesnt has to have all album
MY_BAG_C = {}
# There we have a dict of average of word per song for each artist
AVERAGE_WORD_PER_SONG_PER_ARTIST = {}
# There we have a dict of average of word per song for all music user's library
AVERAGE_WORD_PER_SONG = 0


def change_title(self, path_to_file):
    """
    This function takes out information about author and title of songs from file
    """
    try:
        audio = ID3(path_to_file)
        # Checking if filed was already parsed
        artist = audio['TPE1'].text[0]
        title = audio["TIT2"].text[0]
        label = artist + "," + title
        if label not in LIST_ARTIST_SONGS:
            self.insert_to_right_list_box(artist, title)
            bag_of_words(artist, title)
            LIST_ARTIST_SONGS.append(label)
        else:
            # If was
            print("That was already parsed", " : \n", label)
    except ValueError:
        pass


def bag_of_words(artist_name, song_name):
    """
    Simple bag of words
    We used here a lemmatize to simplify form of words for example running -> run
    And stopwords to remove them from dict
    """
    to_simpler_form = WordNetLemmatizer()
    song = PyLyrics.getLyrics(artist_name, song_name).lower().split()
    song = [word for word in song if word not in stopwords.words('english')]
    song = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in song]
    song = [to_simpler_form.lemmatize(word, 'v') for word in song]
    cnt = Counter(song)
    try:
        MY_BAG[artist_name] = MY_BAG[artist_name] + cnt
        MY_BAG_C[artist_name] += 1
    except KeyError:
        # When we parse new artist we catch the except KeyError
        #  and put new key into dict
        print("Parsing author : ", artist_name, " : Please wait... : )")
        MY_BAG[artist_name] = cnt
        MY_BAG_C[artist_name] = 1


def search_for_simmilar_ver_2(self):
    """
    # Algorithm II #
    We parts our code to have more visibility of what we doing
    There is algorithm which at the beginning catch
    the number of intersections between dicts then use cosine similarity
    """
    my_bag_all = Counter()
    for value in MY_BAG.values():
        my_bag_all += value
    temp = made_group_smaller()
    first_step()
    temp = second_step(temp, my_bag_all)
    temp = fourth_step(temp, my_bag_all)
    temp = fifth_step(temp)
    six_step(self, temp)


def search_for_simmilar_ver_1(self):
    """
    # Algorithm I #
    This algorithm based mainly on cosine similarity
    """
    my_bag_all = Counter()
    for value in MY_BAG.values():
        my_bag_all += value
    temp = made_group_smaller()
    first_step()
    temp = another_try(temp, my_bag_all)
    temp = fourth_step(temp, my_bag_all)
    temp = fifth_step(temp)
    six_step(self, temp)


def made_group_smaller():
    """
    This function is calculating an average of
    words per author and defining max and min
    """
    for artist in sorted(list(MY_BAG), key=lambda s: s.lower()):
        average = len(MY_BAG[artist])/MY_BAG_C[artist]
        AVERAGE_WORD_PER_SONG_PER_ARTIST[artist] = average
        print(artist, " : Average of words per author : ", average)
    print(dict(MY_BAG_C))
    maxs = max(AVERAGE_WORD_PER_SONG_PER_ARTIST.values())
    print("MAX", str(maxs))
    mins = min(AVERAGE_WORD_PER_SONG_PER_ARTIST.values())
    min_max = (mins, maxs)
    print("MIN", str(mins))
    return min_max


def first_step():
    """
    This function loads a date from pickle and put them into dict
    """
    data2 = dict(pickle.load(open("pickleLilEvery.p", 'rb')))
    CATALOG.clear()
    CATALOG.update({key: value for key, value in data2.items()})


def second_step(min_max, my_bag_all):
    """
    This function is defining dictionary of songs with dictionary
    based on amount of shared most popular words in users libraries
    """
    shared_items = {}
    data_from_pickle = dict(pickle.load(
        open("pickleLilFromArtistWordPerSong.p", 'rb')))
    # Here we are making an intersections between
    # all popular words in our library and each song
    # in library of comparing songs
    for key, value in CATALOG.items():
        shared_items[key] = len(set(Counter(value)) & set(my_bag_all))
    # There we choose only authors with average of word
    # per song between max and min of our music library
    if min_max[0] != min_max[1]:
        chosen_data = Counter({key: value for key, value in shared_items.items()
                               if(min_max[1] >= data_from_pickle[key] >= min_max[0]) is True})
    else:
        chosen_data = Counter({key: value for key, value in shared_items.items()})
    keys_list = dict(sorted(chosen_data.most_common(20), key=lambda data: data[1])).keys()
    return list(keys_list)


def another_try(min_max, my_bag_all):
    """
    This function is another option of comparing, this time is depend on cosine similarity.
    The purpose is to find the perfect artist
    """
    shared_items = {}
    data_from_pickle = dict(pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb')))
    for key, value in CATALOG.items():
        shared_items[key] = counter_cosine_similarity(Counter(value), my_bag_all)
    print(shared_items)
    if min_max[0] != min_max[1]:
        chosen_data = Counter({key: value for key, value in shared_items.items()
                               if(min_max[1] >= data_from_pickle[key] >= min_max[0]) is True})
    else:
        chosen_data = Counter({key: value for key, value in shared_items.items()})
    keys_list = dict(sorted(chosen_data.most_common(20), key=lambda data: data[1])).keys()
    return list(keys_list)


def fourth_step(list_chosen, my_bag_all):
    """
    This function make another comparing, this time is depend on cosine similarity.
    The purpose is to find the perfect album from chosen artist
    """
    shared_items_add = {}
    data_from_pickle = pickle.load(open("pickleLil300.p", 'rb'))
    data_from_pickle.update(pickle.load(open("pickleLil500.p", 'rb')))
    data_from_pickle.update(pickle.load(open("pickleLil303.p", 'rb')))
    # We need to pick up some date from pickle
    # with dicts of words from each album of artist
    for key, value in data_from_pickle.items():
        temp = key.split(',', 1)
        if temp[0] in list_chosen:
            shared_items_add[key] = \
                counter_cosine_similarity(Counter(value), my_bag_all)
    # In shared_items[artist,album} we have value of similarity
    temp = Counter({key: value for key, value in shared_items_add.items()
                    if value not in my_bag_all.keys()})
    keys_list = dict(sorted(temp.most_common(20), key=lambda data: data[1])).keys()
    return list(keys_list)


def fifth_step(list_of_keys):
    """
    This function is randomly choosing a song from chosen album
    """
    shared_items_add = {}
    print("Suggest : ")
    for key in list_of_keys:
        temp = key.split(',', 1)
        albums = PyLyrics.getAlbums(singer=temp[0])
        for album in albums:
            if album.name == temp[1]:
                tracks = album.tracks()
                num = random.randint(0, len([track.name for track in tracks])-1)
                print(temp[0], ":", tracks[num].name)
                shared_items_add[key] = tracks[num].name
    return shared_items_add


def six_step(self, shared_items_add):
    """
    This function display chosen titles on GUI
    """
    self.left_list.delete(0, END)
    for key, value in shared_items_add.items():
        temp = key.split(',', 1)
        gui.GUI.insert_to_left_list_box(self, temp[0] + " : " + value)


def counter_cosine_similarity(vector1, vector2):
    """
    This function calculate similarity between vector
    the closer to 1 the more similar are the songs
    """
    # a * b = ||a|| ||b|| cos(theta)
    terms = set(vector1).union(vector2)
    # A * B
    dot_product = sum(vector1.get(key, 0) * vector2.get(key, 0) for key in terms)
    # || A ||
    magnitude_a = math.sqrt(sum(vector1.get(key, 0)**2 for key in terms))
    # || B ||
    magnitude_b = math.sqrt(sum(vector2.get(key, 0)**2 for key in terms))
    return dot_product / (magnitude_a * magnitude_b)
