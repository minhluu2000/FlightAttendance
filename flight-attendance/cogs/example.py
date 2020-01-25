import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ready! 👍\nLogged in as: {self.client.user.name} - {self.client.user.id}\nVersion: {discord.__version__}\n")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

def setup(client):
    client.add_cog(Example(client))