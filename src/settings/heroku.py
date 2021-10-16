from . import *
import os
import django_heroku


if os.environ.get('ENV','development')=='production':
    django_heroku.settings(locals())
