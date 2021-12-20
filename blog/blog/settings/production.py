# production.py
import pathlib
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib(__file__).resolve().parent.parent

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', '.heroku.com']

DATABASES = {
    'default': dj_database_url.config()
}

STATIC_URL = 'https://blog.com/static/'
MEDIA_URL = 'https://blog.com/media/'

django_heroku.settings(locals())