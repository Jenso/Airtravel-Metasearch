DEVELOPMENT = True
DEBUG = TEMPLATE_DEBUG = THUMBNAIL_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR + '/database/test.db',
        'TEST_NAME': PROJECT_DIR + '/database/testest.db',
    }
}

MIDDLEWARE_CLASSES = (
    'core.django-crossdomainxhr-middleware.XsSharing',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

