# production.py
from distutils.log import debug
from re import T
from .settings import *
import dj_database_url
import django_heroku

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True


#DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}



db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

#STATIC_URL = 'https://django-pbpostgres.herokuapp.com/static/'
#MEDIA_URL = 'https://django-pbpostgres.herokuapp.com/media/'

DISABLE_COLLECTSTATIC = 1

django_heroku.settings(locals())