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

    def __init__(self):
        pass

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

    def parse_file_lil_version(self, number_of):
        """
        This function is parsing the lyrics of the songs
        into dicts then put them into pickle files
        """
        if number_of < 0 or number_of > 500:
            number_of = 200
        root = ET.parse('DATA/scrobble.xml').getroot()
        label = ""
        dictionary_per_album = {}
        dictionary_for_artist = {}
        list_of_average = {}
        list_of_average_per_artist = {}
        # dictionary_for_artist = pickle.load(open("pickleLilEvery.p", 'rb'))
        # list_of_average = pickle.load(open("pickleLilWordPerSong.p", 'rb'))
        # list_of_average_per_artist = pickle.load(open("pickleLilFromArtistWordPerSong.p", 'rb'))
        counter = 0
        print(number_of)
        for author in root.findall('.//name'):
            current_artist = ""
            calc_number_of_songs = 0
            counter += 1
            if counter >= number_of:
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
                                dictionary_per_album = self.dict_per_album(dictionary_per_album, label, song)
                                # Counting words per artist
                                dictionary_for_artist = self.dict_for_artist(dictionary_for_artist,
                                                                             current_artist, song)
                            except ValueError:
                                print(" ERROR / There is no such song in PyLyrics")

                        if label in dictionary_per_album:
                            print("Per album " + album.name + " : ", dictionary_per_album[label])
                            list_of_average[label] = sum(dictionary_per_album[label].values())\
                                / calc_number_of_songs_per_album
                            list_of_average_per_artist[current_artist] = \
                                sum(dictionary_for_artist[current_artist]
                                    .values())/calc_number_of_songs
                            self.log_info(list_of_average[label], list_of_average_per_artist[current_artist])

                    except ValueError:
                        print("MEGA ERROR / There is no such album in PyLyrics")
                print("Artist : ", current_artist, "\nAll : ", dictionary_for_artist[current_artist])
            except ValueError:
                print("Connection problem")
        self.put_into_pickles(number_of, dictionary_per_album, dictionary_for_artist,
                              list_of_average, list_of_average_per_artist)

    @staticmethod
    def put_into_pickles(number_of, dictionary_per_album, dictionary_for_artist,
                         list_of_average, list_of_average_per_artist):
        """
            This function is putting dicts into pickles
        """
        with open("DATA/pickleLil" + str(number_of) + ".p", 'wb') as file:
            pickle.dump(dictionary_per_album, file)
        with open("DATA/pickleLilEvery" + ".p", 'wb') as file:
            pickle.dump(dictionary_for_artist, file)
        with open("DATA/pickleLilWordPerSong" + ".p", 'wb') as file:
            pickle.dump(list_of_average, file)
        with open("DATA/pickleLilFromArtistWordPerSong" + ".p", 'wb') as file:
            pickle.dump(list_of_average_per_artist, file)

    @staticmethod
    def dict_for_artist(dictionary_for_artist, current_artist, song):
        """
            This function is putting counter into dicts with label of "current_artist"
        """
        if current_artist not in dictionary_for_artist:
            dictionary_for_artist[current_artist] = Counter(song)
        else:
            dictionary_for_artist[current_artist] =\
                Counter(dictionary_for_artist[current_artist]) + Counter(song)
        return dictionary_for_artist

    @staticmethod
    def dict_per_album(dictionary_per_album, label, song):
        """
            This function is putting counter into dicts with label of "current_artist,album"
        """
        if label not in dictionary_per_album:
            dictionary_per_album[label] = Counter(song)
        else:
            dictionary_per_album[label] = dictionary_per_album[label] + Counter(song)
        return dictionary_per_album

    @staticmethod
    def log_info(info1, info2):
        """
            Logging information
        """
        print("Average of word per song in specific album :: ", info1)
        print("Average of word per song :: ", info2)

