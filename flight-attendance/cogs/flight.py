import discord
from discord.ext import commands

def parse_flight(depart_loc, arrive_loc, depart_time, arrive_time, flight_num):
    pass


class Flight(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def flight(self, ctx, *args):
        depart, arrive = args[1::2]
        await ctx.send(f"Depart: {depart.title()}\nArrive: {arrive.upper() if len(arrive) == 2 else arrive.title()}")


def setup(client):
    client.add_cog(Flight(client))