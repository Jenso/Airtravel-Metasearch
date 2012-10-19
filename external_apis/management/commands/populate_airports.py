from django.core.management.base import BaseCommand, CommandError, AppCommand
from external_apis.models import Airports
import os

class Command(BaseCommand):
    help = 'Populate airports data from dat file'

    def handle(self, *args, **options):

        airports_file = open(os.path.join(os.path.split(os.path.abspath(__file__))[0],"_airports.dat"))
        for airport in airports_file.readlines():
            airport = airport.replace('\"', '')
            airport = airport.replace('\n', '')
            parts = airport.split(",")

            airport = Airports(
                airport_name = parts[1],
                city = parts[2],
                country = parts[3],
                iata = parts[4],
                icao = parts[5],
                latitude = parts[6],
                longitude = parts[7],
                timezone = parts[9],
                dst = parts[10],
                )
            airport.save()
