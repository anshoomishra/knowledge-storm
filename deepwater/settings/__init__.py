import os
from django.core.exceptions import ImproperlyConfigured

environment = os.getenv('DJANGO_ENV') or 'local'

if environment == 'local':
    from .local import *
elif environment == 'prod':
    from .prod import *
else:
    raise ImproperlyConfigured(f"Unknown environment: {environment}")