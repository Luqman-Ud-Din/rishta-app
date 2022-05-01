from .common_settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': env('DB_NAME'),

        'USER': env('DB_USER_NAME'),

        'PASSWORD': env('DB_PASSWORD'),

        'HOST': env('DB_HOST'),

        'PORT': env('DB_PORT'),

    }

}