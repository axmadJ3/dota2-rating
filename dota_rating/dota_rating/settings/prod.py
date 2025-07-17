from decouple import config

from .base import *


DEBUG = False


ADMINS = [
    ('Abdukarimov A', 'email@mydomain.com'),
]


ALLOWED_HOSTS = ['13.62.23.9', 'turbodota.xyz', '109.120.185.211']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
