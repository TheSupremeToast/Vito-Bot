import os
import discord
from discord.ext import commands
import subprocess

from dotenv import load_dotenv
load_dotenv()

USER_ID = os.getenv('USER_ID')

#
# Git puller class
#
class GitPull(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name = 'git_pull')
    async def git_pull(self, ctx):

        def auth(ctx):
            if (int(ctx.author.id) == int(USER_ID)):
                return True
            return False

        if not auth(ctx):
            await (ctx.send('Insufficient Permissions.'))
            return
        try:
            await (ctx.send(subprocess.call('./helpers/git-update.sh')))
        except:
            await (ctx.send('An error occured.'))


# Set up extension
def setup(bot):
    bot.add_cog(GitPull(bot))
