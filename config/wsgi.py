"""
WSGI config for ECOM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import socket

from django.core.wsgi import get_wsgi_application

if socket.gethostname().startswith('live'):
    print(socket.gethostbyname)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')


application = get_wsgi_application()
