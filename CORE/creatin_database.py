"""
    In this file we focus on creating database to comparing songs
"""
from urllib import request
import xml.etree.ElementTree as ET
import pickle
from collections import Counter
import re
from nltk.corpus import stopwords
from PyLyrics import PyLyrics
from nltk.stem.wordnet import WordNetLemmatizer


class CreatingDatabase(object):
    """
        Class responsible for creating DB
    """
    def __init__(self):
        """
            init
        """
        self.dictionary_per_album = {}
        self.dictionary_for_artist = {}
        self.list_of_average = {}
        self.list_of_average_per_artist = {}

    @staticmethod
    def download_list_of_artists():
        """
            This function is downloading the newest list of songs
            from last.fm throw their API
        """
        url = "http://ws.audioscrobbler.com/2.0/" \
            "?method=chart.gettopartists&api_key=d70d8067d56b2afc78942623d4256817&limit=1000"
        request.urlretrieve(url, "scrobble.xml")

    @staticmethod
    def do_the_dicts(artist, name):
        """
            Operation on lyrics
        """
        song = PyLyrics.getLyrics(artist, name).lower().split()
        song = [word for word in song if word not in stopwords.words('english')]
        song = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in song]
        # changing word for simple form running -> run
        song = [WordNetLemmatizer().lemmatize(word, 'v') for word in song]
        return song

    def refresh_dicts(self):
        """
            This function is cleaning dicts
        """
        self.list_of_average.clear()
        self.list_of_average_per_artist.clear()
        self.dictionary_per_album.clear()
        self.reads_dicts()

    def reads_dicts(self):
        """
            This function is reading dicts from pickles
        """
        self.dictionary_for_artist = pickle.load(open("DATA/pickleLilEvery.pkl", 'rb'))
        self.list_of_average = pickle.load(open("DATA/pickleLilWordPerSong.pkl", 'rb'))
        self.list_of_average_per_artist = \
            pickle.load(open("DATA/pickleLilFromArtistWordPerSong.pkl", 'rb'))

    def parse_file(self, number_of, number_from):
        """
            This function is parsing the lyrics of the songs
            into dicts then put them into pickle files
        """
        if number_of < 0 or number_of > 1000:
            number_of = 200
        root = ET.parse('DATA/scrobble.xml').getroot()
        label = ""
        if number_from != 0:
            self.refresh_dicts()
        counter = 0
        for author in root.findall('.//name'):
            if counter < number_from:
                counter += 1
            else:
                current_artist = ""
                calc_number_of_songs = 0
                counter += 1
                if counter > number_of:
                    break
                print("Artist: ", author.text, counter)
                # going to albums
                try:
                    for album in PyLyrics.getAlbums(author.text):
                        # going to tracks in album
                        calc_number_of_songs_per_album = 0
                        try:
                            print("ALBUM", author.text, " : ", album.name, " Parsing... ")
                            for track in PyLyrics.getTracks(album):
                                # going to lyric in song
                                try:
                                    current_artist = track.artist
                                    label = current_artist + "," + album.name
                                    print(track.artist, " : ", album.name, " : ", track.name, " : ")
                                    # operation on lyrics
                                    song = self.do_the_dicts(current_artist, track.name)
                                    # Counting songs per artist
                                    calc_number_of_songs += 1
                                    calc_number_of_songs_per_album += 1
                                    # Counting words per album
                                    self.dict_per_album(label, song)
                                    # Counting words per artist
                                    self.dict_for_artist(current_artist, song)
                                except ValueError:
                                    print(" ERROR / There is no such song in PyLyrics")

                            if label in self.dictionary_per_album:
                                print("Per album " + album.name + " : ",
                                      self.dictionary_per_album[label])
                                self.list_of_average[label] = \
                                    sum(self.dictionary_per_album[label].values())\
                                    / calc_number_of_songs_per_album
                                self.list_of_average_per_artist[current_artist] = \
                                    sum(self.dictionary_for_artist[current_artist]
                                        .values())/calc_number_of_songs
                                self.__log_info(self.list_of_average[label],
                                              self.list_of_average_per_artist[current_artist])

                        except (ValueError, UnboundLocalError):
                            print("MEGA ERROR / There is no such album in PyLyrics")
                    if current_artist in self.dictionary_for_artist:
                        print("Artist : ",
                              current_artist, "\nAll : ", self.dictionary_for_artist[current_artist])
                except ValueError:
                    print("Connection problem / There is no such artist in PyLyrics")
        self.put_into_pickles(number_of)

    def put_into_pickles(self, number_of):
        """
            This function is putting dicts into pickles
        """
        with open("DATA/pickleLil" + str(number_of) + ".pkl", 'wb') as file:
            pickle.dump(self.dictionary_per_album, file)
        with open("DATA/pickleLilEvery" + ".pkl", 'wb') as file:
            pickle.dump(self.dictionary_for_artist, file)
        with open("DATA/pickleLilWordPerSong" + ".pkl", 'wb') as file:
            pickle.dump(self.list_of_average, file)
        with open("DATA/pickleLilFromArtistWordPerSong" + ".pkl", 'wb') as file:
            pickle.dump(self.list_of_average_per_artist, file)
        self.check()

    @staticmethod
    def check():
        """
            This function is printing a pickle
        """
        try_it = pickle.load(open("DATA/pickleLilEvery.pkl", 'rb'))
        print(try_it)

    def dict_for_artist(self, current_artist, song):
        """
            This function is putting counter into dicts with label of "current_artist"
        """
        if current_artist not in self.dictionary_for_artist:
            self.dictionary_for_artist[current_artist] = Counter(song)
        else:
            self.dictionary_for_artist[current_artist] =\
                Counter(self.dictionary_for_artist[current_artist]) + Counter(song)
        return self.dictionary_for_artist

    def dict_per_album(self, label, song):
        """
            This function is putting counter into dicts with label of "current_artist,album"
        """
        if label not in self.dictionary_per_album:
            self.dictionary_per_album[label] = Counter(song)
        else:
            self.dictionary_per_album[label] = self.dictionary_per_album[label] + Counter(song)

    @staticmethod
    def __log_info(info1, info2):
        """
            Logging information
        """
        print("Average of word per song in specific album :: ", info1)
        print("Average of word per song :: ", info2)

