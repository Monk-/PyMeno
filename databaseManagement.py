from urllib import request
from PyLyrics import *
import xml.etree.ElementTree as ET
import pickle


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
