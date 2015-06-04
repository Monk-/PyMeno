"""
    In this file we have function to split lyrics of songs with user's library
    into dicts and looks for other similarly songs
"""
from collections import Counter
from PyLyrics import PyLyrics
import pickle
import math
import random
import argparse
from googleapiclient.discovery import build


class FindMusic(object):
    # YouTube API
    DEVELOPER_KEY = "AIzaSyCn9Pk4vWC8LjjIKqol5gkku20DI0IRurU"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    # There we have a dict of average of word per song for each artist
    AVERAGE_WORD_PER_SONG_PER_ARTIST = {}
    # There we have a dict of average of word per song for all music user's library
    AVERAGE_WORD_PER_SONG = 0
    # Important to not put the same values into users library again
    LIST_ARTIST_SONGS = []
    # kind of temporary
    CATALOG = Counter()

    MY_BAG = {}
    # Dict of songs per artist
    # Its have to be that way because user doesnt has to have all album
    MY_BAG_C = {}

    def __init__(self, my_bag, my_bag_c):
        self.MY_BAG = my_bag
        self.MY_BAG_C = my_bag_c

    def search_for_simmilar_ver_2(self):
        """
            # Algorithm II #
            We parts our code to have more visibility of what we doing
            There is algorithm which at the beginning catch
            the number of intersections between dicts then use cosine similarity
        """
        my_bag_all = Counter()
        for value in self.MY_BAG.values():
            my_bag_all += value
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver1(temp, my_bag_all)
        temp = self.fourth_step(temp, my_bag_all)
        temp = self.fifth_step(temp)
        return self.six_step(temp)

    def search_for_simmilar_ver_1(self):
        """
            # Algorithm I #
            This algorithm based mainly on cosine similarity
        """
        my_bag_all = Counter()
        for value in self.MY_BAG.values():
            my_bag_all += value
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver2(temp, my_bag_all)
        temp = self.fourth_step(temp, my_bag_all)
        temp = self.fifth_step(temp)
        return self.six_step(temp)

    def search_for_simmilar_ver_3(self):
        """
            # Algorithm III #
        """
        temp = self.made_group_smaller()
        self.first_step()
        temp = self.second_step_ver3(temp)
        temp = self.fifth_step(temp)
        return self.six_step(temp)

    def made_group_smaller(self):
        """
            This function is calculating an average of
            words per author and defining max and min
        """
        for artist in sorted(list(self.MY_BAG), key=lambda s: s.lower()):
            average = len(self.MY_BAG[artist])/self.MY_BAG_C[artist]
            self.AVERAGE_WORD_PER_SONG_PER_ARTIST[artist] = average
            print(artist, " : Average of words per author : ", average)
        print(dict(self.MY_BAG_C))
        maxs = max(self.AVERAGE_WORD_PER_SONG_PER_ARTIST.values())
        print("MAX", str(maxs))
        mins = min(self.AVERAGE_WORD_PER_SONG_PER_ARTIST.values())
        min_max = (mins, maxs)
        print("MIN", str(mins))
        return min_max

    def first_step(self):
        """
            This function loads a date from pickle and put them into dict
        """
        data2 = dict(pickle.load(open("DATA/pickleLilEvery.p", 'rb')))
        self.CATALOG.clear()
        self.CATALOG.update({key: value for key, value in data2.items()})

    def second_step_ver1(self, min_max, my_bag_all):
        """
            This function is defining dictionary of songs with dictionary
            based on amount of shared most popular words in users libraries
        """
        shared_items = {}
        data_from_pickle = dict(pickle.load(
            open("DATA/pickleLilFromArtistWordPerSong.p", 'rb')))
        # Here we are making an intersections between
        # all popular words in our library and each song
        # in library of comparing songs
        for key, value in self.CATALOG.items():
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

    def second_step_ver2(self, min_max, my_bag_all):
        """
            This function is another option of comparing, this time is depend on cosine similarity.
            The purpose is to find the perfect artist
        """
        shared_items = {}
        data_from_pickle = dict(pickle.load(open("DATA/pickleLilFromArtistWordPerSong.p", 'rb')))
        for key, value in self.CATALOG.items():
            shared_items[key] = self.counter_cosine_similarity(Counter(value), my_bag_all)
        print(shared_items)
        if min_max[0] != min_max[1]:
            chosen_data = Counter({key: value for key, value in shared_items.items()
                                   if(min_max[1] >= data_from_pickle[key] >= min_max[0]) is True})
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
        data_from_pickle = pickle.load(open("DATA/pickleLil300.p", 'rb'))
        data_from_pickle.update(pickle.load(open("DATA/pickleLil500.p", 'rb')))
        data_from_pickle.update(pickle.load(open("DATA/pickleLil303.p", 'rb')))
        for key, value in self.MY_BAG.items():
            shared_items_album.clear()
            for key_lib, value_lib in data_from_pickle.items():
                s = key_lib.replace('_', ' ')
                temp = s.split(',', 1)
                if key != temp[0]:
                    shared_items_album[key_lib] = self.counter_cosine_similarity(Counter(value), value_lib)

            [shared_items.append(x) for x in list(dict(sorted(Counter(shared_items_album).most_common(40),
                                                              key=lambda data: data[1])).keys())]
        data_from_pickle = dict(pickle.load(open("DATA/pickleLilFromArtistWordPerSong.p", 'rb')))
        chosen_data = [key for key in shared_items
                       if(min_max[1] >= data_from_pickle[key.split(',', 1)[0]] >= min_max[0]) is True]
        return chosen_data

    def fourth_step(self, list_chosen, my_bag_all):
        """
            This function make another comparing, this time is depend on cosine similarity.
            The purpose is to find the perfect album from chosen artist
        """
        shared_items_add = {}
        data_from_pickle = pickle.load(open("DATA/pickleLil300.p", 'rb'))
        data_from_pickle.update(pickle.load(open("DATA/pickleLil500.p", 'rb')))
        data_from_pickle.update(pickle.load(open("DATA/pickleLil303.p", 'rb')))
        # We need to pick up some date from pickle
        # with dicts of words from each album of artist
        for key, value in data_from_pickle.items():
            temp = key.split(',', 1)
            if temp[0] in list_chosen:
                shared_items_add[key] = \
                    self.counter_cosine_similarity(Counter(value), my_bag_all)
        # In shared_items[artist,album} we have value of similarity
        temp = Counter({key: value for key, value in shared_items_add.items()
                        if value not in my_bag_all.keys()})
        keys_list = dict(sorted(temp.most_common(20), key=lambda data: data[1])).keys()
        return list(keys_list)

    @staticmethod
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
        return shared_items_add

    @staticmethod
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

    def youtube_search(self, to_search):
        """
            This function finds url to our songs throw Youtube API
        """
        parse = argparse.ArgumentParser()
        parse.add_argument("--q", help="Search term", default=to_search)
        parse.add_argument("--max-results", help="Max results", default=25)
        args = parse.parse_args()
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)

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
        except UnicodeEncodeError:
            pass