import os 
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

RENDER_FRONT_EXTERNAL_HOSTNAME = os.environ.get('RENDER_FRONT_EXTERNAL_HOSTNAME')
if RENDER_FRONT_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_FRONT_EXTERNAL_HOSTNAME)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = 'RENDER' not in os.environ

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL='/static/'
if not DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'

BASEURL = 'https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

CORS_ALLOWED_ORIGINS = ['https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))]
CORS_ALLOWED_ORIGINS.append(os.environ.get('RENDER_FRONT_EXTERNAL_HOSTNAME'))
CORS_ALLOW_CREDENTIALS = True
ALLOWED_ORIGINS = ['https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))]
ALLOWED_ORIGINS.append(os.environ.get('RENDER_FRONT_EXTERNAL_HOSTNAME'))
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS.copy()

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256