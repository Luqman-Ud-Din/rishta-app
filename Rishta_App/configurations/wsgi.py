"""
WSGI config for Rishta_App project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from .common_settings import env
from django.core.wsgi import get_wsgi_application

if env('ENVIRONMENT') == 'PROD':
    configurations = 'configurations.prod_settings'
else:
    configurations = 'configurations.dev_settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', configurations)

application = get_wsgi_application()
