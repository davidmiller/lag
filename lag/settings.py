from socket import gethostname
#from unipath import FSPath as Path
import os
ADMINS = (
     ('David Miller', 'david@larapel.com'),
)

MANAGERS = ADMINS

HOSTNAME = gethostname()
PSQL_HOSTS = ['bosch', 'parmenides', 'rasputin']
DEBUG_HOSTS = ['parmenides', 'jung', 'rasputin', 'bosch']

# Paths
ROOT = os.path.dirname(__file__)
import sys
sys.path.append(ROOT)

BUILDOUT_ROOT = os.path.dirname(ROOT)
MEDIA_ROOT = os.path.join(ROOT, 'static')
STATICFILES_DIRS = (
    MEDIA_ROOT,
    )
STATIC_URL = '/m/'
ADMIN_MEDIA_PREFIX = '/m/admin/'
if HOSTNAME == 'bosch':
    ADMIN_MEDIA_PREFIX = '/media/'
# Debug
DEBUG = False
if HOSTNAME in DEBUG_HOSTS:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG


# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'lag',
        'USER': 'django',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}
if HOSTNAME not in PSQL_HOSTS:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['default']['NAME'] = ROOT.child('lag.db')
    DATABASES['default']['USER'] = ''
    DATABASES['default']['PASSWORD'] = ''

    # I18N
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
SECRET_KEY = 'q5r$$z4t(xy27q28^vtng)12ml)h!16v1^z%xr+2@yys67e)#p'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'lag.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django.contrib.gis',
#    'south',
    'django_extensions',
    'django_mobile',
    'lag.registration',
    'lag.players',
    'lag.locations',

)

# Registration and accounts
ACCOUNT_ACTIVATION_DAYS = 2
DEFAULT_FROM_EMAIL = "david@deadpansincerity.com"
LOGIN_REDIRECT_URL = "/home/"
AUTH_PROFILE_MODULE = 'players.Player'

