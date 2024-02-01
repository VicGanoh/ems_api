from .base import *
from dotenv import dotenv_values

config = dotenv_values(".env")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.get("DB_NAME"),
        "USER": config.get("USER"),
        "HOST": config.get("HOST"),
        "PASSWORD": config.get("DB_PASS"),
        "PORT": config.get("PORT"),
    }
}

SECRET_KEY = config.get("SECRET_KEY")