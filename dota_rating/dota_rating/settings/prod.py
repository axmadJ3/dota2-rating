from decouple import config

from .base import *


DEBUG = False


ADMINS = [
    ('Abdukarimov A', 'email@mydomain.com'),
]


ALLOWED_HOSTS = ['13.62.23.9']


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
