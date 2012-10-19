# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Airports'
        db.create_table('external_apis_airports', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('airport_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('iata', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('icao', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('timezone', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('dst', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('external_apis', ['Airports'])


    def backwards(self, orm):
        # Deleting model 'Airports'
        db.delete_table('external_apis_airports')


    models = {
        'external_apis.airports': {
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
            'timezone': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['external_apis']