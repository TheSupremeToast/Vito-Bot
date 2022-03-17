import os
from os.path import exists
import time
import datetime
import logging

import lyricsgenius as lg

from helpers.lyrics import readartists

from dotenv import load_dotenv
load_dotenv()

client_token = os.getenv('CLIENT_ACCESS_TOKEN')

logger = logging.getLogger(__name__)
fh = logging.FileHandler(filename='logs/' + str(datetime.date.today()) + '.log')
fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s \n%(message)s\n'))
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

# authenticate genius client
genius = lg.Genius(client_token, skip_non_songs = True, 
        remove_section_headers = False)

# fail counter for potential timeouts
fail_count = 0

#
# get top songs for artists
# stores in files
#
# WARNING: this function takes a long time to run if the output dir is empty
#
# TODO - append additional songs to artist files
# - fix issue where doesn't correctly generate files when running as background process
#
def generate_artistfiles():
    global fail_count
    artists = readartists()
    song = 0
    
    # for each artist in list/file generate a file with artistname and top (8) songs
    for artist in artists:
        # start logging
        logger.info('\n \n \n--- REQUEST START --- \n')
        logger.info(artist)
        logger.info('\n----------\n')

        # check if an artist file already exists
        if exists(f'./output/artists/{artist}.txt'):
            # if an artist file is empty allow it to be filled
            if (os.stat(f'output/artists/{artist}.txt').st_size == 0):
                logger.info(f'\n\n {artist}.txt was empty, recreating \n') 
            # otherwise log it exists and move on
            else:
                logger.info(f'--- {artist}.txt Exists ---')
                continue

        artistfile = open(f'./output/artists/{artist}.txt', 'w')
        try: 
            logger.info(f'Searching for top songs for {artist}')
            # get top songs and write full lyrics to files
            songs = (genius.search_artist(artist,max_songs=10,sort='popularity')).songs
            s = [song.lyrics for song in songs]
            artistfile.write('\n\nSongStart:\n'.join(s))
            artistfile.close()
            # print(f'{artist}.txt finished')
            logger.info(f'{artist}.txt written')
            
            # more logger stuff
            # logger.info('\n \n--- Full Lyrics Start --- \n')
            # logger.info(s)
            # logger.info('\n --- Full Lyrics End --- \n')
        # handle the timeout error that can happen from the genius search
        except:
            #print('\nFetch Failed: Trying Again...\n')
            fail_count += 1
            if fail_count >= 5:
                #print(f'\nFetch Failed ({fail_count}) Times: Breaking...\n')
                return
            retry = open('./retry.txt', 'a')
            retry.write(f'\nerror on {artist}, retrying')
            retry.close()
            logger.exception('RETRY FUNCTION')
            generate_artistfiles()

        # reset fail count after loop ends
        fail_count = 0
