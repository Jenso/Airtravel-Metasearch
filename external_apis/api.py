from tastypie import authorization
from tastypie_mongoengine import resources
#from test_app import documents
"""
class PersonResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Person.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
"""

from tastypie import fields
from tastypie.authorization import Authorization

from tastypie_mongodb.resources import MongoDBResource, Document

class DocumentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    currency = fields.CharField(attribute="currency", null=True)
    total_price = fields.ListField(attribute="total-price", null=True)

    class Meta:
        resource_name = "trips"
        list_allowed_methods = ["delete", "get", "post"]
        authorization = Authorization()
        object_class = Document
        collection = "test_collection" # collection name
