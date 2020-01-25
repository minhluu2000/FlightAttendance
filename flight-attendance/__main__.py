import os
import discord
from discord.ext import commands

TOKEN = 'NjcwNzAzOTE4MjM3NjE0MDgw.XiygSg.xpRGVxgh_Ry6T78so2Hk3u3DfqQ'

client = commands.Bot(command_prefix='.')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('flight-attendance/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN, bot=True)