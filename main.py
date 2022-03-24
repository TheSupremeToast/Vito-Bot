import os
import random
import time

import discord
from discord.ext import commands

from cogs import *

#
# TODO: file launching/closing commands through the bot to host?
# Fortune: get random lyric/2 random lines
#


from dotenv import load_dotenv
load_dotenv()
# get discord bot token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID = os.getenv('USER_ID')

# auth for discord bot client
# client = discord.Client()

# Define command prefix
bot = commands.Bot(command_prefix = 'vito ')

## VERY IMPORTANT ##
# loads all extension (.py) files from ./commands/
load_cogs(bot)


#
# Run when bot connects
#
@bot.event
async def on_ready():
    # print(f'{client.user} has connected to Discord!')
    print(f'Connected to Discord!')


#
# respond to message prompts
#
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
 
    # joke response
    if 'gabagool' in  message.content.lower():
        await message.channel.send('*gabagool*')

    # allow commands to work past on_message override
    await bot.process_commands(message)


#
# Only allow certain users to use given command
#
async def authenticate(msg):
    if int(msg.author.id) == int(USER_ID):
        return True
    else:
        await msg.channel.send('Insufficient Permissions.')
        return False


#
# Reload all external command files
#
@bot.command(name = 'reload_cogs')
async def reloadcogs(ctx):
    if (not await authenticate(ctx)):
        await ctx.send('Insufficient Permissions.')
        pass
    try:
        reload_cogs(bot) 
        await ctx.send('Cogs reloaded.')
    except:
        await ctx.send('An error occured.')


# client.run(TOKEN)
bot.run(TOKEN)
