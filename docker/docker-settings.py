DEBUG = True

CORS_ALLOWED_ORIGINS = ['http://10.5.0.1:5173', 'http://10.5.0.1:8000', 'http://10.5.0.1:3000', 'http://localhost:3000', 'http://localhost:8000']
CSRF_ALLOWED_ORIGINS = ['http://10.5.0.1:5173', 'http://10.5.0.1:8000', 'http://10.5.0.1:3000', 'http://localhost:3000', 'http://localhost:8000']
CORS_ALLOW_METHODS = ('DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT')
CORS_ALLOW_HEADERS = ('authorization', 'content-type')
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD':'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/static/media/'
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['http://10.5.0.1:8000', 'http://10.5.0.1:5173', 'http://10.5.0.1:3000', 'http://localhost:3000', 'http://localhost:8000']

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

BASEURL = 'http://10.5.0.1:3000'
BACKEND_TEST_PORT = 8000
FRONTEND_TEST_PORT = 5173

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
