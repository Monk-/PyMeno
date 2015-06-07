"""
    In this file we focus on creating database to comparing songs
"""
from urllib import request
import xml.etree.ElementTree as Et
import pickle
from collections import Counter
import re
from nltk.corpus import stopwords
from PyLyrics import PyLyrics
from nltk.stem.wordnet import WordNetLemmatizer
import logging


class CreatingDatabase(object):
    """
        Class responsible for creating DB
    """
    static_label = ""

    def __init__(self):
        """
            init
        """
        self.logger = logging.getLogger(__name__)
        self.dictionary_per_album = {}
        self.dictionary_for_artist = {}
        self.list_of_average = {}
        self.list_of_average_per_artist = {}
        self.calc_number_of_songs = 0
        self.calc_number_of_songs_per_album = 0

    def download_list_of_artists(self):
        """
            This function is downloading the newest list of songs
            from last.fm throw their API
        """
        url = "http://ws.audioscrobbler.com/2.0/" \
              "?method=chart.gettopartists&api_key=d70d8067d56b2afc78942623d4256817&limit=1000"
        request.urlretrieve(url, "data/scrobble.xml")
        self.logger.debug('downloading scrobble list')

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
        self.calc_number_of_songs = 0
        self.calc_number_of_songs_per_album = 0
        CreatingDatabase.static_label = ""

    def reads_dicts(self):
        """
            This function is reading dicts from pickles
        """
        self.dictionary_for_artist = pickle.load(open("data/pickleLilEvery.pkl", 'rb'))
        self.list_of_average = pickle.load(open("data/pickleLilWordPerSong.pkl", 'rb'))
        self.list_of_average_per_artist = \
            pickle.load(open("data/pickleLilFromArtistWordPerSong.pkl", 'rb'))

    def parse_file(self, number_of, number_from):
        """
            This function is parsing the lyrics of the songs
            into dicts then put them into pickle files
        """
        if number_of < 0 or number_of > 1000:
            number_of = 200
        root = Et.parse('data/scrobble.xml').getroot()
        if number_from != 0:
            self.refresh_dicts()
        counter = 0
        for author in root.findall('.//name'):
            self.calc_number_of_songs = 0
            if counter < number_from:
                counter += 1
            else:
                current_artist = ""
                self.calc_number_of_songs = 0
                counter += 1
                if counter > number_of:
                    break
                print("Artist: ", author.text, counter)
                # going to albums
                try:
                    for album in PyLyrics.getAlbums(author.text):
                        # going to tracks in album
                        self.calc_number_of_songs_per_album = 0
                        try:
                            print("ALBUM", author.text, " : ", album.name, " Parsing... ")
                            for track in PyLyrics.getTracks(album):
                                # going to lyric in song
                                self.operation_per_song(track, album)
                        except (ValueError, UnboundLocalError):
                            self.logger.error('no such album in PyLyrics :: %s', author.text,
                                              exc_info=True)
                    if current_artist in self.dictionary_for_artist:
                        print("Artist : ",
                              current_artist, "\nAll : ",
                              self.dictionary_for_artist[current_artist])
                except (ValueError, ConnectionError):
                    self.logger.error('Connection problem / no such artist in PyLyrics :: %s',
                                      author.text, exc_info=True)
        self.put_into_pickles(number_of)

    def put_into_pickles(self, number_of):
        """
            This function is putting dicts into pickles
        """
        with open("data/pickleLil" + str(number_of) + ".pkl", 'wb') as file:
            pickle.dump(self.dictionary_per_album, file)
        with open("data/pickleLilEvery" + ".pkl", 'wb') as file:
            pickle.dump(self.dictionary_for_artist, file)
        with open("data/pickleLilWordPerSong" + ".pkl", 'wb') as file:
            pickle.dump(self.list_of_average, file)
        with open("data/pickleLilFromArtistWordPerSong" + ".pkl", 'wb') as file:
            pickle.dump(self.list_of_average_per_artist, file)
        self.check()

    def calculate_average(self, current_artist):
        """
            This method calculates average
        """
        if CreatingDatabase.static_label in self.dictionary_per_album:
            self.list_of_average[CreatingDatabase.static_label] = \
                sum(self.dictionary_per_album[CreatingDatabase.static_label].values()) \
                / self.calc_number_of_songs_per_album
            self.list_of_average_per_artist[current_artist] = \
                sum(self.dictionary_for_artist[current_artist].values()) / self.calc_number_of_songs
            self.__log_info(self.list_of_average[CreatingDatabase.static_label],
                            self.list_of_average_per_artist[current_artist])

    def operation_per_song(self, track, album):
        """
            This method makes operation on song
        """
        try:
            current_artist = track.artist
            CreatingDatabase.static_label = current_artist + "," + album.name
            print(track.artist, " : ", album.name, " : ", track.name, " : ")
            # operation on lyrics
            song = self.do_the_dicts(current_artist, track.name)
            # Counting songs per artist
            self.calc_number_of_songs += 1
            self.calc_number_of_songs_per_album += 1
            # Counting words per album
            self.dict_per_album(song)
            # Counting words per artist
            self.dict_for_artist(current_artist, song)
            self.calculate_average(current_artist)
        except ValueError:
            self.logger.error('no such song in PyLyrics', exc_info=True)

    @staticmethod
    def check():
        """
            This function is printing a pickle
        """
        try_it = pickle.load(open("data/pickleLilEvery.pkl", 'rb'))
        print(try_it)

    def dict_for_artist(self, current_artist, song):
        """
            This function is putting counter into dicts with label of "current_artist"
        """
        if current_artist not in self.dictionary_for_artist:
            self.dictionary_for_artist[current_artist] = Counter(song)
        else:
            self.dictionary_for_artist[current_artist] = \
                Counter(self.dictionary_for_artist[current_artist]) + Counter(song)
        return self.dictionary_for_artist

    def dict_per_album(self, song):
        """
            This function is putting counter into dicts with label of "current_artist,album"
        """
        if CreatingDatabase.static_label not in self.dictionary_per_album:
            self.dictionary_per_album[CreatingDatabase.static_label] = Counter(song)
        else:
            self.dictionary_per_album[CreatingDatabase.static_label] = \
                self.dictionary_per_album[CreatingDatabase.static_label] + Counter(song)

    @staticmethod
    def __log_info(info1, info2):
        """
            Logging information
        """
        print("Average of word per song in specific album :: ", info1)
        print("Average of word per song :: ", info2)
