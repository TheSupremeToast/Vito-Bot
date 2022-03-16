import random
import os
import asyncio
import discord
from discord.ext import commands
from helpers.lyrics import *

#
# Song game command class
#
# TODO - remove printing of ##embed and 'songstart' - might require fixes in other files
#
class SongGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#
# Song game command
#
# uses my lyrics fetcher to grab song lyrics/song/artist
# user tries to guess the name of the song or the artist that made it
#
    @commands.command(name = 'songgame')
    async def playsonggame(self, ctx):
        chorus = choose_chorus()
        lyrics = chorus[0]
        artistname = chorus[1]
        songname = chorus[2]
        # print(songname, artistname)
        msg = 0 
        await ctx.send(f'Guess the name of the following song, or the artist that made it:\n{lyrics}')

        # check if the user is the same as the message author and in the same channel
        def check(msg):
            return (msg.author.id == ctx.author.id and msg.channel == ctx.channel)
      
        # function for checking user input against song/artist name
        async def check_answer(msg, ctx):
            # take user input
            try:
                # print(check(ctx))
                msg = await self.bot.wait_for('message', 
                        check=check, timeout = 30)
                # print (msg.content)
            except asyncio.TimeoutError:
                await ctx.send('You ran out of time!')
                return

            # check code
            correct = False
            if songname.lower() in msg.content.lower():
                # case for correct name guess
                await ctx.send('Congratulations, you guessed the song name!')
                correct = True
            if artistname.lower() in msg.content.lower():
                await ctx.send('Congratulations, you guessed the artist name!')
                correct = True
            else:
                # case for wrong guessg
                await ctx.send('Incorrect, try again.')
                return False
            return correct


        # run the get and check answer function 3 times or until correct
        flag = False
        tries = 0
        while (not flag and tries < 3):
            flag = await check_answer(msg, ctx)
            tries += 1
        if (flag == False):
            await ctx.send('You ran out of tries.')
        await ctx.send(f'Song: {songname}, by: {artistname}')

# Set up extension
def setup(bot):
    bot.add_cog(SongGame(bot))
