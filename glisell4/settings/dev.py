from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x=w594xfj3&qt%-+=7v$4df8ap!o638%i0q(b$=v)og4eigxd1'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# LEAFLET_CONFIG = {
#     # conf here
# }

# GEOS_LIBRARY_PATH = 'C:/OSGeo4W64/bin/geos_c.dll'
WAGTAIL_ADDRESS_MAP_CENTER = 'Santo Domingo, Dominican Republic'
WAGTAIL_ADDRESS_MAP_ZOOM = 10
# EASY_MAPS_CENTER = (-41.3, 32)

try:
    from .local import *
except ImportError:
    pass
