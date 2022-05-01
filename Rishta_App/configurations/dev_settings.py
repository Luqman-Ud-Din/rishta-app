from .common_settings import *


DEBUG = True
ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{BASE_DIR}/{env("DB_NAME")}',
    }
}
