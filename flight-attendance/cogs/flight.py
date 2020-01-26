import json
from asyncio import sleep
from datetime import datetime as dt

import discord
import requests
from discord.ext import commands

# THE DESTINATION MUST ALWAYS BE FROM DALLAS TO CHICAGO

class AA_Wrapper:

    PLACE_ABR = dict(
        Dallas = "DFW",
        Tokyo = "NRT",
        LA = "LAX",
        Houston = "IAH",
        Chicago = "ORD"
    )
    __response = ""
    data = ""

    @classmethod
    def user_request(cls, **kwargs):
        date = f"{dt.now().strftime('%Y-%m-%d')}" if not kwargs["date"] else kwargs["date"]
        origin = kwargs["origin"] if "origin" in kwargs else ""
        destination = kwargs["destination"] if "destination" in kwargs else "" 
        cls.__response = requests.get(f"https://flightattendance.herokuapp.com/flights?date={date}&origin={cls.PLACE_ABR.get(origin,'')}&destination={cls.PLACE_ABR.get(destination,'')}").text

    @classmethod
    def process_request(cls):
        cls.data = json.loads(cls.__response)[:3]
        
        clean_data = []
        for element in cls.data:
            clean_data.append(dict(
                flightNumber = element["flightNumber"],
                origin = element["origin"]["city"],
                destination = element["destination"]["city"],
                duration = element["duration"]["locale"],
                departureTime = element["departureTime"],
                arrivalTime = element["arrivalTime"]
            ))
        return clean_data


def parse_flight(date, destination, origin):
    '''

    '''
    if date.lower() in ('tonight', 'today'): #origin= Dallas, Destination = Chicago
        date = None

    AA_Wrapper.user_request(date=date, origin=origin, destination=destination)
    flights = AA_Wrapper.process_request()
    return flights


class Flight(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @staticmethod
    def make_embed(n, flightNumber, duration, origin, departureTime, destination, arrivalTime):
        embed = discord.Embed(title=f"Flight {n}", colour=discord.Colour(0xbe90b9))

        embed.add_field(name="Flight No", value=f"{flightNumber}", inline=False)
        embed.add_field(name="Duration", value=f"{duration}", inline=False)
        embed.add_field(name="Depart", value=f"{origin}\n{departureTime}", inline=True)
        embed.add_field(name="Arrive", value=f"{destination}\n{arrivalTime}", inline=True)

        return embed

    @staticmethod
    def final_choice(flightNumber, duration, origin, departureTime, destination, arrivalTime):
        embed = discord.Embed(colour=discord.Colour(0xbe90b9), description=f"Economy Class\nAirbus A320\nFlight Time:{duration} ")

        embed.set_image(url="https://media.discordapp.net/attachments/670703730697699362/670866843887599646/qr-code_4.png")
        embed.set_thumbnail(url="https://i.pinimg.com/originals/9f/92/b9/9f92b92b83bf3426b37b7b0e45ab2d94.png")

        embed.add_field(name="Duration", value=f"{duration}", inline=False)
        embed.add_field(name="Flight No.", value=f"{flightNumber}", inline=False)
        embed.add_field(name="Departure", value=f"{origin}", inline=True)
        embed.add_field(name="Departure Time", value=f"{departureTime}", inline=True)
        embed.add_field(name="Arrival", value=f"{destination}", inline=False)
        embed.add_field(name="Arrival Time", value=f"{arrivalTime}", inline=True)

        return embed
    
    @commands.command()
    async def flight(self, ctx, *args):
        if not args:
            def check(m): return m.author == ctx.message.author
            def check_flight(m):
                if m.content.isdigit():
                    return int(m.content) in range(1,4)
                else:
                    return False

            flight_info = [] # [date, destination, origin]
            flight_info = ['today', 'Chicago', 'Dallas']
            dialog = (
                f"When would you like to fly {ctx.message.author.mention}?",
                "Sounds great! Where would you like to fly?",
                "Alrighty! Where would you like to depart from?")
            
            
            # for msg in dialog:
            #     await ctx.send(msg)
            #     response = await self.client.wait_for('message', check=check)
            #     flight_info.append(response.content.title())
            # else:

            #     flight_results = parse_flight(*flight_info)
            #     await ctx.send(flight_results)

            flight_results = parse_flight(*flight_info)
            for n,flight_result in enumerate(flight_results, start=1):
                card = Flight.make_embed(n,**flight_result)
                await ctx.send(embed=card)
            else:
                await ctx.send("Which flight would you like?")
                flight_option = await self.client.wait_for('message', check=check_flight)
                flight_card = Flight.final_choice(**flight_results[int(flight_option.content)-1])
                await ctx.send(embed=flight_card)
            
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
