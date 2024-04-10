from .base import *


ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("HOST"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "PORT": os.environ.get("PORT"),
    }
}

SECRET_KEY = os.environ.get("SECRET_KEY")