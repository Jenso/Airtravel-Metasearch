from django.conf.urls import patterns, include, url

from tastypie.api import Api
from core.api import AirportResource

general_api = Api(api_name='general')
general_api.register(AirportResource())

urlpatterns = patterns('',
    (r'^api/',
            include(general_api.urls)),
)
