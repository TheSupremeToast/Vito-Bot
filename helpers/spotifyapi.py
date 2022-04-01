# import os
# from dotenv import load_dotenv
import pandas as pd

import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# load_dotenv()
# client = os.getenv('SPOTIPY_CLIENT_ID')
# secret = os.getenv('SPOTIPY_CLIENT_SECRET')
# uri = os.getenv('SPOTIPY_REDIRECT_URI')
#
# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Helper functions for spotify api calls

####################

# Track id functions

#
# convert dict information into track ids
#
def get_track_ids(tracks):
    track_ids = []
    for song in tracks['items']:
        # print(song['artist'])
        # print(song)
        track_ids.append(song['id'])
        
    return track_ids

#
# convert song ids into readable information
#
def get_track_features(user, id):
    meta = user.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']

    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info

#
# create dataframe containing track information obtained from get_track_features()
#
def convert_to_df(user, track_ids):
    tracks = []
    for i in range(len(track_ids)):
        track = get_track_features(user, track_ids[i])
        tracks.append(track)

        df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 
            'spotify_url', 'album_cover'])
    df.to_csv(f'output/top_tracks.csv')
    return df

#####################

# Artist id functions

#
# convert dict infromation into artist ids
#
def get_artist_ids(artists):
    artist_ids = []
    for artist in artists['items']:
        artist_ids.append(artist['id'])
    return artist_ids

# TODO

# get genres of all songs in a dataframe (based on artist genre)

#####################

#
# get track_info for a playlist
# TODO - fix
#
def playlist_to_df(user, playlist_link):
    playlist_URI = playlist_link.split('/')[-1].split('?')[0]
    print(playlist_URI)
    list_URIs = user.playlist_tracks(playlist_URI)
    # print(list_URIs)
    tracks = get_track_ids(list_URIs)
    df = convert_to_df(tracks)
    return df

# Get playlist audio features
# TODO use seaborn to make it a heatmap
#https://towardsdatascience.com/reverse-engineering-spotify-wrapped-ai-using-python-452b58ad1a62
def playlist_features_to_df(user, playlist_link = None):
    # change this line for more universal applicability
    playlist_link = 'https://open.spotify.com/playlist/5ggFp2EDeRSdslnW0T0rlv?si=e44d6bcd7bf0426b'
    playlist_URI = playlist_link.split('/')[-1].split('?')[0]
    list_URIs = user.playlist_tracks(playlist_URI)['items']
    track_uris = []
    for x in list_URIs:
        track_uris.append(x['track']['uri'])

    af = user.audio_features(track_uris)[0]
    features = pd.DataFrame.from_dict(af, orient='index').T
    for i in range(1, len(track_uris)):
        af = user.audio_features(track_uris)[i]
        new_feature = pd.DataFrame.from_dict(af, orient='index').T
        features = features.append(new_feature)
        features = features.reset_index().drop('index', axis = 1)
        features = features.drop(columns=['type', 'id', 'uri', 'track_href', 'analysis_url'])
    return features

