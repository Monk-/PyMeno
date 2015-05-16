from urllib import request
from PyLyrics import *
import xml.etree.ElementTree as ET
import pickle
from collections import Counter
import re
from mutagen.id3 import ID3
from nltk.corpus import stopwords
from PyLyrics import *
from nltk.stem.wordnet import WordNetLemmatizer

def download_list_of_artists():
    request.urlretrieve("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=d70d8067d56b2afc78942623d4256817&limit=1000", "scrobble.xml")


def parseFile(number_of):
    if number_of < 0 or number_of > 500:
        number_of = 200
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    list3 = []
    dicto = {}
    counter = 0
    print(number_of)
    for x in root.findall('.//name'):
        if counter >= number_of:
            break
        counter += 1
        print(x.text, counter)
        try:
            for g in PyLyrics.getAlbums(x.text):
                try:
                    for track in PyLyrics.getTracks(g):
                        try:
                            dicto[track.artist + "," + track.name] = PyLyrics.getLyrics(track.artist, track.name).lower()
                            #append(PyLyrics.getLyrics(track.artist, track.name).lower())
                            #print(track.artist, track.name)
                        except ValueError:
                            print(track.artist, track.name, " ERROR ")
                            pass
                except:
                    print("MEGA ERROR")
        except:
            print("GIGA ERROR")
    with open("pickle" + str(number_of) + ".p", 'wb') as f:
        pickle.dump(dicto, f)


def parse_file_lil_version(number_of):
    if number_of < 0 or number_of > 500:
        number_of = 200
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    lemmatizer = WordNetLemmatizer()
    dicto = {}
    dicto_for_artist = pickle.load(open("pickleLilEvery.p", 'rb'))
    counter = 0
    print(number_of)
    for x in root.findall('.//name'):
        if counter > 99:
            counter += 1
            if counter >= number_of:
                break
            print("Artist: ", x.text, counter)
            try:
                for g in PyLyrics.getAlbums(x.text):
                    try:
                        for track in PyLyrics.getTracks(g):
                            try:
                                print(track.artist, track.name, " Parsing... ")
                                song = PyLyrics.getLyrics(track.artist, track.name).lower().split()
                                song = [word for word in song if word not in stopwords.words('english')]
                                song = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in song]
                                #changing word for simple form running -> run
                                song = [lemmatizer.lemmatize(x, 'v') for x in song]
                                dicto[track.artist + "," + track.name] = Counter(song)
                                try:
                                    print("here")
                                    dicto_for_artist[track.artist] = Counter(dicto_for_artist[track.artist]) + Counter(song)
                                except:
                                    print("not here")
                                    dicto_for_artist[track.artist] = Counter(song)
                                print(dicto[track.artist + "," + track.name])
                                print("Artists", dicto_for_artist[track.artist])
                            except ValueError:
                                print(track.artist, track.name, " ERROR ")
                                pass
                    except:
                        print("MEGA ERROR")
            except:
                print("GIGA ERROR")
        else:
            counter += 1
    with open("pickleLil" + str(number_of) + ".p", 'wb') as f:
        pickle.dump(dicto, f)
    with open("pickleLilEvery" + ".p", 'wb') as l:
        pickle.dump(dicto_for_artist, l)


def get_music_stats():
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    data2 = pickle.load(open("pickleLilEvery.p", 'rb'))
    for x in root.findall('.//name'):
        try:
            print(x.text, " : Summary words : ", len(data2[x.text]),  data2[x.text].most_common(10))
        except:
            pass


def get_music_stats_by_album():
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    try:
        data2 = pickle.load(open("pickleLil50.p", 'rb'))
        data1 = pickle.load(open("pickleLil100.p", 'rb'))
        data2.update(data1)
        for x in root.findall('.//name'):
            print("Artist: ", x.text)
            try:
                for g in PyLyrics.getAlbums(x.text):
                    try:
                        for track in PyLyrics.getTracks(g):
                            try:
                                print(track.name, " : Summary words : ", len(data2[track.artist + "," + track.name]),
                                      data2[track.artist + "," + track.name].most_common(5))
                            except:
                                pass
                    except:
                        pass
            except:
                pass
    except:
        print("Nothing")
