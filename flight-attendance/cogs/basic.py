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
                cog_name = filename[:-3]

                if cog_name.title() not in self.client.cogs: # Load the cog instead of reloading it if it wasn't loaded
                    self.client.load_extension(f'cogs.{cog_name}')
                else:
                    self.client.reload_extension(f'cogs.{cog_name}')

        else: await ctx.send('Reload Successful! :+1:')

    @commands.command()
    async def cogs(self, ctx):
        await ctx.send(f"{[*self.client.cogs]}")


def setup(client):
    client.add_cog(Basic(client))