from TravelX.settings import *

DEBUG = TEMPLATE_DEBUG = THUMBNAIL_DEBUG = False
PRODUCTION = True

AWS_ACCESS_KEY_ID = 'AKIAJHCGEY6XAXXOSYXA'
AWS_SECRET_ACCESS_KEY = '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'

STATIC_URL = 'http://travelx.s3-website-eu-west-1.amazonaws.com/'
MEDIA_URL = 'http://travelx.s3-website-eu-west-1.amazonaws.com/'

DEFAULT_FILE_STORAGE = STATICFILES_STORAGE = ('storages.backends'
                                              '.s3boto.S3BotoStorage')

AWS_STORAGE_BUCKET_NAME = 'travelx'
