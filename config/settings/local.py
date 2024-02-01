from .base import *
from dotenv import dotenv_values

config = dotenv_values(".env")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.get("BASE_DB_NAME"),
        "USER": config.get("BASE_USER"),
        "HOST": config.get("BASE_HOST"),
        "PASSWORD": config.get("BASE_DB_PASS"),
        "PORT": config.get("PORT"),
    }
}

SECRET_KEY = config.get("SECRET_KEY")