import os
from core.base import *
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY_DJANGO")
DEBUG = False

ALLOWED_HOSTS = ['161.35.87.89']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("NAME_DB"),
        'HOST': 'localhost',
        'PORT': 5432,
        'USER': os.getenv("USER_DB"),
        'PASSWORD': os.getenv("PASS_DB")
    }
}
