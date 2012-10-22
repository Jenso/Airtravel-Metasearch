from django.db import models

class Airports(models.Model):
    airport_name = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    iata = models.CharField(max_length=3, blank=True)
    icao = models.CharField(max_length=4, blank=True)
    latitude = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=200, blank=True)
    timezone = models.CharField(max_length=20, blank=True)
    dst = models.CharField(max_length=20, blank=True)    
