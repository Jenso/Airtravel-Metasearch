# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Airports.timezone'
        db.delete_column('core_airports', 'timezone')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Airports.timezone'
        raise RuntimeError("Cannot reverse this migration. 'Airports.timezone' and its values cannot be restored.")

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
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['core']