import os
import pandas as pd
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import discord
from discord.ext import commands

from helpers.spotifyauth import *
from helpers.spotifyapi import *

# pull needed tokens and keys from .env file
load_dotenv()
client = os.getenv('SPOTIPY_CLIENT_ID')
secret = os.getenv('SPOTIPY_CLIENT_SECRET')
uri = os.getenv('SPOTIPY_REDIRECT_URI')


'''
spotipy-wrapped commands class
'''
class SpotifyCmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #
    # login function
    # TODO - Doesn't worl
    #
    @commands.command(name = 'spotify_login')
    async def spotifyLogin(self, ctx):
        return authLogin()

    #
    # get users top tracks
    #
    # TODO: allow more than just user defined in .env
    #
    @commands.command(name = 'ttracks')
    async def getUserTopTracks(self, ctx, timeframe = 'medium_term'):
        async with ctx.typing():
            scope = 'user-top-read'
            user = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope))
            trackdict = user.current_user_top_tracks(limit = 25, time_range = timeframe)
            trackids = get_track_ids(trackdict)
            tracks = convert_to_df(user, trackids)
            out = f"Your Top Tracks:\n" + tracks[['name', 'artist']].to_string(index = False)
        await ctx.send(out)


    #
    # get users top artists
    #
    # TODO: allow more than just user defined in .env
    #       also make it actually work
    #
    @commands.command(name = 'tartists')
    async def getUserTopArtists(self, ctx, timeframe = 'medium_term'):
        async with ctx.typing():
            scope = 'user-top-read'
            user = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope))
            artistdict = user.current_user_top_artists(time_range = timeframe)
            artistids = get_track_ids(artistdict)
            artists = convert_to_df(user, artistids)
            out = f"Your Top Artists:\n" + tracks[['name','artist']].to_string(index = False)
        await ctx.send(out)



# setup function for extension
def setup(bot):
    bot.add_cog(SpotifyCmds(bot))
