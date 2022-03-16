import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from helpers.generateartists import *

USER_ID = os.getenv('USER_ID')

# authenticate the command user is contained in .env 
async def auth(self, ctx):
    if (int(ctx.author.id) == int(USER_ID)):
        return True
    return False

#
# Class containing all the verse and song commands (not songgame)
#
class SongCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #
    # Add an artist to the artist file
    #
    @commands.command()
    async def add_artist(self, ctx, *args):
        if not await auth(self, ctx):
            await ('Insufficient Permissions.')
            return
        name = ''
        for arg in args:
            name += arg + ' '
        name = name.rstrip()
        with open('input/artists.txt', 'a') as f:
            f.write(f'{name}\n')
        await ctx.send(f'{name} added.')
        return

    #
    # clear the requests file
    #
    @commands.command()
    async def clear_requests(self, ctx):
        if await auth(self, ctx):
            with open('./input/requests.txt', 'w') as f:
                f.truncate(0)
                await ctx.send('Requests Cleared.')
        return

    #
    # Generate artist files containing lyrics based on artists.txt
    #
    @commands.command()
    async def gen_artistfiles(self, ctx):
        if not await auth(self, ctx):
            await ctx.send('Insufficient Permissions.')
            return

        authB = await ctx.send('Authenitcation Success')
        work = await ctx.send('Working...')

        generate_artistfiles()
        await authB.delete()
        await work.delete()
        await ctx.send('Finished.')
        return

    #
    # print out the artists.txt file
    #
    @commands.command()
    async def get_artists(self, ctx):
        await ctx.send(file = discord.File('./input/artists.txt'))
        return

    #
    # print out the requests file
    #
    @commands.command()
    async def get_requests(self, ctx):
        await ctx.send(file = discord.File('./input/requests.txt'))
        return

    #
    # remove an artist from artists.txt
    #
    @commands.command()
    async def remove_artist(self, ctx, *args):
        if not await auth(self, ctx):
            await ctx.send('Insufficient Permissions.')
            return
        name = ''
        for arg in args:
            name += arg + ' '
        name = name.rstrip()
        with open('input/artists.txt', 'r') as f:
            lines = f.readlines()
        with open('input/artists.txt', 'w') as f:
            for line in lines:
                if line.strip('\n') != name:
                    f.write(line)
        await ctx.send(f'{name} removed.')
        return

    #
    # remove a request from the requests file
    #
    @commands.command()
    async def remove_request(self, ctx, *args):
        if await auth(self, ctx):
            name = ''
            for arg in args:
                name += arg + ' '
            name = name.rstrip()
            with open('input/requests.txt', 'r') as f:
                lines = f.readlines()
            with open('input/requests.txt', 'w') as f:
                for line in lines:
                    if line.strip('\n') != name:
                        f.write(line)
            await ctx.send(f'{name} removed from requests.')
        return

    #
    # add artist to the requests file
    #
    @commands.command()
    async def request_artist(self, ctx, *args):
        name = ''
        for arg in args:
            name += arg + ' '
        name = name.rstrip()
        with open('./input/requests.txt', 'a') as f:
            f.write(f'{name}\n') 
            await ctx.send(f'{name} requested, pending review.')
        return





# setup function for extension
def setup(bot):
    bot.add_cog(SongCmds(bot))
