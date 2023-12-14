ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CSRF_ALLOWED_ORIGINS = ["http://localhost:5173"]
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

APIS = {
    'authentication': 'http://10.5.0.1:8000',
    'base': 'http://10.5.0.1:8000',
    'booth': 'http://10.5.0.1:8000',
    'census': 'http://10.5.0.1:8000',
    'mixnet': 'http://10.5.0.1:8000',
    'postproc': 'http://10.5.0.1:8000',
    'store': 'http://10.5.0.1:8000',
    'visualizer': 'http://10.5.0.1:8000',
    'voting': 'http://10.5.0.1:8000',
}

BASEURL = 'http://10.5.0.1:8000'
BACKEND_TEST_PORT = 8000
FRONTEND_TEST_PORT = 5173

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
