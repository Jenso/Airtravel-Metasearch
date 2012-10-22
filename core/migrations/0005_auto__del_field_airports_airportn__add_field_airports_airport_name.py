# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Airports.airportn'
        db.delete_column('core_airports', 'airportn')

        # Adding field 'Airports.airport_name'
        db.add_column('core_airports', 'airport_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Airports.airportn'
        db.add_column('core_airports', 'airportn',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Deleting field 'Airports.airport_name'
        db.delete_column('core_airports', 'airport_name')


    models = {
        'core.airports': {
            'Meta': {'object_name': 'Airports'},
            'airport_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'dst': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'iata': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'icao': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['core']