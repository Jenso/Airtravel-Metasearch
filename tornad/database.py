import mongoengine
import os

MONGO_DATABASE_NAME = 'trip'
db = mongoengine.connect(MONGO_DATABASE_NAME)

# To know if we should query api's or use the local XML file
RESULT_LIMIT = 30

PRODUCTION = DEVELOPMENT = USE_LOCAL_XML = False

if os.environ.has_key('PRODUCTION'):
    PRODUCTION = True
else:
    DEVELOPMENT = True
    USE_LOCAL_XML = True
