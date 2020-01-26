import discord
import os
from discord.ext import commands

class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ready! 👍\nLogged in as: {self.client.user.name} - {self.client.user.id}\nVersion: {discord.__version__}\n")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def reload(self, ctx):
        for filename in os.listdir('flight-attendance/cogs'):
            if filename.endswith('.py'):
                
                self.client.reload_extension(f'cogs.{filename[:-3]}')
        else:
            await ctx.send('Reload Successful! :+1:')

def setup(client):
    client.add_cog(Basic(client))