from tastypie import authorization
from tastypie_mongoengine import resources

import bson
import mongoengine

class Trip(mongoengine.Document):
    meta = {
        'allow_inheritance': False,
        'collection': 'trips',
    }
    currency = mongoengine.StringField()
    outbound = mongoengine.DictField()
    inbound = mongoengine.DictField()
    total_price = mongoengine.StringField(db_field="total-price")
    deeplink = mongoengine.StringField()

class DocumentResource(resources.MongoEngineResource):
    class Meta:
        queryset = Trip.objects.order_by('total-price')
        allowed_methods = ('get')
        authorization = authorization.Authorization()
        #collection = "test_collection" # collection name
        resource_name = "trips"


from core.models import Airports
from tastypie.resources import ModelResource
from django.db.models import Q

class AirportResource(ModelResource):
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(AirportResource, self).build_filters(filters)

        if('custom_query' in filters):
            query = filters['custom_query']
            qset = (
                Q(iata__istartswith=query) |
                Q(airport_name__istartswith=query) |
                Q(city__istartswith=query) |
                Q(country__istartswith=query)
                )
            orm_filters.update({'custom': qset})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(AirportResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered
    
    class Meta:
        resource_name = 'airports'
        queryset = Airports.objects.all()
        #excludes = ['user']
        allowed_methods = ['get']
        limit = 50
        #max_limit = 0
