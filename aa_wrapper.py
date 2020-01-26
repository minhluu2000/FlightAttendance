# Insert code here
# Things I can get from AA API:
#   - date
#   - origin

# What to get: fnumber, departure, destination, dep_time, arriv_time, dep_date, arriv_date

import requests
import json
from datetime import datetime as dt

class AA_Wrapper:

    PLACE_ABR = dict(
        Dallas = "DFW",
        Tokyo = "NRT",
        LA = "LAX",
        Houston = "IAH"
    )
    __response = ""
    data = ""

    @classmethod
    def user_request(cls, **kwargs):
        date = kwargs["date"] if "date" in kwargs else f"{dt.now().strftime('%Y-%m-%d')}"
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