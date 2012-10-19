import mongoengine

MONGO_DATABASE_NAME = 'trip'
db = mongoengine.connect(MONGO_DATABASE_NAME)

# Used to know if we should query api's or use the local XML file
USE_LOCAL_XML = True
