import os
import discord
from discord.ext import commands

# helper function to load files from commands
def get_cogs():
    os.chdir('commands')
    cog_files = []
    file_count = 0
    for file in os.scandir():
        if (file.path.endswith('.py') and file.is_file()):
            file_count += 1
            pos = file.path.index('.py')
            filename = file.path[2:pos]
            cog_files.append(f'commands.{filename}')
    os.chdir('../')
    return cog_files


#
# helper function to import extension command files
#
def load_cogs(bot):
    cog_files = get_cogs() # uncomment when testing all files
    # cog_files = ['commands.example'] # list of manually imported cog files
    for cog_file in cog_files:
        bot.load_extension(cog_file)

#
# helper function to reload cog files
#
def reload_cogs(bot):
    for cog_file in get_cogs():
        bot.reload_extension(cog_file)
