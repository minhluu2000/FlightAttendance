from asyncio import sleep
import discord
from discord.ext import commands

def parse_flight(depart_loc, arrive_loc, depart_time, arrive_time, flight_num):
    pass


class Flight(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def flight(self, ctx, *args):
        if not args:
            def check(m): return m.author == ctx.message.author

            flight_info = []
            
            dialog = (
                f"When would you like to fly {ctx.message.author.mention}?",
                "Sounds great! Where would you like to fly?",
                "Alrighty! Where would you like to depart from?")
            
            
            for msg in dialog:
                await ctx.send(msg)
                response = await self.client.wait_for('message', check=check)
                flight_info.append(response.content)
            else:
                await ctx.send(flight_info)
            
        else:
            if (args[0].lower() != 'from') and (args[2].lower() != 'to'):
                await ctx.send('Usage: .flight from {location} to {location}')
            else:
                depart, arrive = args[1], ' '.join(args[3:])
                async with ctx.typing():
                    await sleep(2)
                    await ctx.send(f"Depart: {depart.title()}\nArrive: {arrive.upper() if len(arrive) == 2 else arrive.title()}")


def setup(client):
    client.add_cog(Flight(client))