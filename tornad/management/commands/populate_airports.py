from django.core.management.base import BaseCommand, CommandError, AppCommand
from core.models import Airports
import os

class Command(BaseCommand):
    help = 'Populate airports data from dat file'

    def handle(self, *args, **options):

        airports_file = open("tornad/data/airports.dat")
        for airport in airports_file.readlines():
            airport = airport.replace('\"', '')
            airport = airport.replace('\n', '')
            parts = airport.split(",")

            # only take airports with IATA-code
            iata = parts[4]
            if not iata:
                continue
            
            airport = Airports(
                airport_name = parts[1],
                city = parts[2],
                country = parts[3],
                iata = iata,
                icao = parts[5],
                latitude = parts[6],
                longitude = parts[7],
                timezone = parts[9],
                dst = parts[10],
                )
            airport.save()
