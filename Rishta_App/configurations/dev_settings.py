from .common_settings import *


DEBUG = True
ALLOWED_HOSTS=['127.0.0.1', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{BASE_DIR}/{env("DB_NAME")}',
    }
}
