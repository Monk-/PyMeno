"""
    In this file we have function to split lyrics of songs with user's library
    into dicts and looks for other similarly songs
"""
from collections import Counter
from PyLyrics import PyLyrics
import pickle
import math
import random


class FindMusic(object):
    """
        FindMusic class is looking for similar music to user's library
    """

    def __init__(self, my_bag_a, my_bag_ca):
        """
            init
        """
        # There we have a dict of average of word per song for each artist
        self.average_word_per_song_artist = {}
        # There we have a dict of average of word per song for all music user's library
        self.average_word_per_song = 0
        # Important to not put the same values into users library again
        self.list_artist_songs = []
        # kind of temporary
        self.catalog = Counter()

        self.my_bag = my_bag_a
        self.my_bag_c = my_bag_ca

    def search_for_simmilar_ver_2(self, queue):
        """
            # Algorithm II #
            We parts our code to have more visibility of what we doing
            There is algorithm which at the beginning catch
            the number of intersections between dicts then use cosine similarity
        """
        my_bag_all = Counter()
        for value in self.my_bag.values():
            my_bag_all += value
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver1(temp, my_bag_all)
        temp = self.fourth_step(temp, my_bag_all)
        temp = self.fifth_step(temp, queue)
        return temp

    def search_for_simmilar_ver_1(self, queues):
        """
            # Algorithm I #
            This algorithm based mainly on cosine similarity
        """
        my_bag_all = Counter()
        for value in self.my_bag.values():
            my_bag_all += value
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver2(temp, my_bag_all)
        temp = self.fourth_step(temp, my_bag_all)
        temp = self.fifth_step(temp, queues)
        return temp

    def search_for_simmilar_ver_3(self, queue):
        """
            # Algorithm III #
        """
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver3(temp)
        temp = self.fifth_step(temp, queue)
        return temp

    def made_group_smaller(self):
        """
            This function is calculating an average of
            words per author and defining max and min
        """
        for artist in sorted(list(self.my_bag), key=lambda art: art.lower()):
            average = len(self.my_bag[artist])/self.my_bag_c[artist]
            self.average_word_per_song_artist[artist] = average
            print(artist, " : Average of words per author : ", average)
        print(dict(self.my_bag_c))
        maxs = max(self.average_word_per_song_artist.values())
        print("MAX", str(maxs))
        mins = min(self.average_word_per_song_artist.values())
        min_max = (mins, maxs)
        print("MIN", str(mins))
        return min_max

    def first_step(self):
        """
            This function loads a date from pickle and put them into dict
        """
        data2 = dict(pickle.load(open("data/pickleLilEvery.pkl", 'rb')))
        self.catalog.clear()
        self.catalog.update({key: value for key, value in data2.items()})

    def second_step_ver1(self, min_max, my_bag_all):
        """
            This function is defining dictionary of songs with dictionary
            based on amount of shared most popular words in users libraries
        """
        shared_items = {}
        data_pickle = dict(pickle.load(
            open("data/pickleLilFromArtistWordPerSong.pkl", 'rb')))
        # Here we are making an intersections between
        # all popular words in our library and each song
        # in library of comparing songs
        for key, value in self.catalog.items():
            shared_items[key] = len(set(Counter(value)) & set(my_bag_all))
        # There we choose only authors with average of word
        # per song between max and min of our music library
        if min_max[0] != min_max[1]:
            chosen_data = Counter({key: value for key, value in shared_items.items()
                                   if(min_max[1] >= data_pickle[key] >= min_max[0]) is True})
        else:
            chosen_data = Counter({key: value for key, value in shared_items.items()})
        keys_list = dict(sorted(chosen_data.most_common(20), key=lambda data: data[1])).keys()
        return list(keys_list)

    def second_step_ver2(self, min_max, my_bag_all):
        """
            This function is another option of comparing, this time is depend on cosine similarity.
            The purpose is to find the perfect artist
        """
        shared_items = {}
        data_pickle = dict(pickle.load(open("data/pickleLilFromArtistWordPerSong.pkl", 'rb')))
        for key, value in self.catalog.items():
            shared_items[key] = self.similarity(Counter(value), my_bag_all)
        print(shared_items)
        if min_max[0] != min_max[1]:
            chosen_data = Counter({key: value for key, value in shared_items.items()
                                   if(min_max[1] >= data_pickle[key] >= min_max[0]) is True})
        else:
            chosen_data = Counter({key: value for key, value in shared_items.items()})
        keys_list = dict(sorted(chosen_data.most_common(20), key=lambda data: data[1])).keys()
        return list(keys_list)

    def second_step_ver3(self, min_max):
        """
            This function is another option of comparing, this time is depend on cosine similarity.
            The purpose is to find the perfect artist similar to another in user's library
        """
        shared_items = []
        shared_items_album = {}
        data_pickle = pickle.load(open("data/pickleLil300.pkl", 'rb'))
        data_pickle.update(pickle.load(open("data/pickleLil500.pkl", 'rb')))
        data_pickle.update(pickle.load(open("data/pickleLil303.pkl", 'rb')))
        data_pickle.update(pickle.load(open("data/pickleLil600.pkl", 'rb')))
        for key, value in self.my_bag.items():
            shared_items_album.clear()
            for key_lib, value_lib in data_pickle.items():
                phrase = key_lib.replace('_', ' ')
                temp = phrase.split(',', 1)
                if key != temp[0]:
                    shared_items_album[key_lib] = self.similarity(Counter(value), value_lib)

            # [shared_items.append(x)
            #  for x in list(dict(sorted(Counter(shared_items_album).most_common(40),
            #                           key=lambda data: data[1])).keys())]
        data_pickle = dict(pickle.load(open("data/pickleLilFromArtistWordPerSong.pkl", 'rb')))
        chosen_data = [key for key in shared_items
                       if(min_max[1] >= data_pickle[key.split(',', 1)[0]] >= min_max[0]) is True]
        return chosen_data

    def fourth_step(self, list_chosen, my_bag_all):
        """
            This function make another comparing, this time is depend on cosine similarity.
            The purpose is to find the perfect album from chosen artist
        """
        shared_items_add = {}
        data_pickle = pickle.load(open("data/pickleLil300.pkl", 'rb'))
        data_pickle.update(pickle.load(open("data/pickleLil500.pkl", 'rb')))
        data_pickle.update(pickle.load(open("data/pickleLil303.pkl", 'rb')))
        data_pickle.update(pickle.load(open("data/pickleLil600.pkl", 'rb')))
        # We need to pick up some date from pickle
        # with dicts of words from each album of artist
        for key, value in data_pickle.items():
            temp = key.split(',', 1)
            if temp[0] in list_chosen:
                shared_items_add[key] = \
                    self.similarity(Counter(value), my_bag_all)
        # In shared_items[artist,album} we have value of similarity
        temp = Counter({key: value for key, value in shared_items_add.items()
                        if value not in my_bag_all.keys()})
        keys_list = dict(sorted(temp.most_common(20), key=lambda data: data[1])).keys()
        return list(keys_list)

    @staticmethod
    def fifth_step(list_of_keys, queues):
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
                    queues.put(temp[0], ":", tracks[num].name)
                    print(temp[0], ":", tracks[num].name)
                    shared_items_add[key] = tracks[num].name
        return shared_items_add

    @staticmethod
    def similarity(vector1, vector2):
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

