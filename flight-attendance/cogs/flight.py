from asyncio import sleep
import discord
from discord.ext import commands

def parse_flight(depart_loc, arrive_loc, depart_time, arrive_time, flight_num):
    '''
    embed = discord.Embed(colour=discord.Colour(0xbe90b9), description="Economy Class\nAirbus A320\nFlight Time:{Trip_Time} ")

    embed.set_image(url="https://media.discordapp.net/attachments/670703730697699362/670866843887599646/qr-code_4.png")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/9f/92/b9/9f92b92b83bf3426b37b7b0e45ab2d94.png")

    embed.add_field(name="Depature Date", value="{Depature_Date}", inline=True)
    embed.add_field(name="Flight No.", value="{Flight_Number}", inline=True)
    embed.add_field(name="Departure", value="{Departure_Location}", inline=True)
    embed.add_field(name="Departure Time", value="{Departure_Time}", inline=True)
    embed.add_field(name="Arrival", value="{Arrival_Location}", inline=True)
    embed.add_field(name="Arrival Time", value="{Arrival_Time}", inline=True)

    await bot.say(embed=embed)
    '''


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