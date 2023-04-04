import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-d#r(ziqb*@8n$*k%5*&14oz&lzao#@16mwh)j+axl21%vyt%bf'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", 'sveshshop.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sveshdb',
        'USER': 'sveshuser',
        'PASSWORD': 'rbhz',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
