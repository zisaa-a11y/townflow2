SECRET_KEY = 'test'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = []
MIDDLEWARE = []
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
