import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '$l_8qaj143h5e(l3fhwukzz2olk(cs5h_i=f*ajoux@3zdc(lt'
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATIC_ROOT = '/Library/WebServer/Documents/gab/static/'
MEDIA_ROOT = '/Library/WebServer/Documents/gab/media/'
