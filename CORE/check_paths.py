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
import logging


class MakeBagOfWords(object):
    """
        This class searches user's library and turns lyrics into dicts
    """

    def __init__(self):
        """
            init
        """
        self.logger = logging.getLogger(__name__)
        # Important to not put the same values into users library again
        self.list_artist_songs = []
        # Dict of words per artist
        self.my_bag = {}
        # Dict of songs per artist
        # Its have to be that way because user doesnt has to have all album
        self.my_bag_c = {}
        self.last_path = ""

    def check_if_refresh(self, path):
        """
            This function checks if values need to be erased
        """
        if self.last_path != path:
            self.last_path = path
            self.clear_bag_of_words()

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
            if label not in self.list_artist_songs:
                # self.insert_to_right_list_box(artist, title)
                self.bag_of_words(artist, title)
                self.list_artist_songs.append(label)
            else:
                # If was
                print("That was already parsed", " : \n", label)
        except (ValueError, UnicodeEncodeError):
            self.logger.error("cannot read the file")
            print("cannot read the file")
        return self.list_artist_songs

    def bag_of_words(self, artist_name, song_name):
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
        if artist_name not in self.my_bag:
            print("Parsing author : ", artist_name, " : Please wait... : )")
            self.my_bag[artist_name] = cnt
            self.my_bag_c[artist_name] = 1
        else:
            self.my_bag[artist_name] = self.my_bag[artist_name] + cnt
            self.my_bag_c[artist_name] += 1

    def clear_bag_of_words(self):
        """
            This function clears dicts
        """
        self.list_artist_songs.clear()
        self.my_bag.clear()
        # Dict of songs per artist
        # Its have to be that way because user doesnt has to have all album
        self.my_bag_c.clear()
