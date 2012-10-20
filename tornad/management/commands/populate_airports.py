from django.core.management.base import BaseCommand, CommandError, AppCommand
from core.models import Airports
import os

def format_timezone(str):
    """
    From timezone in -1 or 1, to -0100 or 0100
    """
    if "-" in str:
        formatted_str = "-"
        str = str[1:]
    else:
        formatted_str = "+"

    if len(str) == 1:
        formatted_str += "0" + str + ":00"
    else:
        formatted_str += str + ":00"
        
    return formatted_str

class Command(BaseCommand):
    help = 'Populate airports data from dat file'

    def handle(self, *args, **options):
        for airport in Airports.objects.all():
            airport.delete()
            
        airports_file = open("tornad/data/airports.dat")
        for airport in airports_file.readlines():
            airport = airport.replace('\"', '')
            airport = airport.replace('\n', '')
            parts = airport.split(",")

            # only take airports with IATA-code
            iata = parts[4]
            if not iata:
                continue

            timezone = format_timezone(parts[9])
            airport = Airports(
                airport_name = parts[1],
                city = parts[2],
                country = parts[3],
                iata = iata,
                icao = parts[5],
                latitude = parts[6],
                longitude = parts[7],
                timezone = timezone,
                dst = parts[10],
                )
            airport.save()
