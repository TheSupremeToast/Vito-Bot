import lyricsgenius as lg
import random
import os
from os.path import exists
import time
import datetime
import logging


# set up logging
logger = logging.getLogger(__name__)
fh = logging.FileHandler(filename='logs/' + str(datetime.date.today()) + '.log')
fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s \n%(message)s\n'))
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

#
# Read the artists file into a list
#
def readartists():
    artists = []
    with open('input/artists.txt', 'r') as f:
        artists = [line.rstrip('\n') for line in f]
        return artists


#
# randomly choose arist -> song -> chorus 
#
# TODO:
# fix cases for songs with no choruses
# add logging
#
def choose_chorus():
    artists = readartists() 

    # choose artist
    artist = random.choice(artists)

    # open artist lyrics file generated from get_artists()
    lyric_file = open(f'./output/artists/{artist}.txt', 'r')

    # get indices of lines where '[Chorus' appears
    indices = []
    # also get indices where new songs start
    songs = [0]
    i = 0
    lines = lyric_file.readlines()
    for line in lines: 
        if ('[Chorus' in line):
            indices.append(i)
        if ('SongStart:' in line):
            songs.append(i+1)
        i += 1

    index = random.choice(indices)

    # implement loop to determine current song
    currentsong = 'None'
    for songindex in songs:
        if (songindex <= index):
            splitsong = lines[songindex].split(' Lyrics[')
            currentsong = splitsong[0]
        else:
            break


    # get all lines of the chorus to return
    temp = index
    lyrics = ''
    j = 0 
    while (True):
        temp += 1
        if (temp == i+1):
            break
        if ('[' in lines[temp]):
            break 
        if (temp == i):
            lines[temp] = lines[temp].removesuffix('Embed')
        else:
            lyrics += lines[temp]    
        j += 1 

    # return chorus of given song
    # - also returns artist and song names
    return ([lyrics, artist, currentsong])
