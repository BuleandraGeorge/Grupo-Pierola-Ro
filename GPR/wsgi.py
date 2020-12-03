"""WSGI config for GPR project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GPR.settings')

application = get_wsgi_application()
