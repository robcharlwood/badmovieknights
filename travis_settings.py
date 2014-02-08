# import django deps
from badmovieknights.settings import *


# travis ci database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'travis',
        'PASSWORD': '',
        'NAME': 'badmovieknights',
    }
}
