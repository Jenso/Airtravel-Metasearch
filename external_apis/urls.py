from django.conf.urls import patterns, include, url

from tastypie.api import Api
from external_apis.api import DocumentResource

profile_api = Api(api_name='trips')
profile_api.register(DocumentResource())

urlpatterns = patterns('',
    (r'^api/',
            include(profile_api.urls)),
)
