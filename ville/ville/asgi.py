"""
ASGI config for ville project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import channels.asgi


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ville.settings')

channel_layer = channels.asgi.get_channel_layer()
application = get_asgi_application()
