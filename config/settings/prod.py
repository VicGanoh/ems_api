from .base import *
from dotenv import dotenv_values

config = dotenv_values(".env")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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

SECRET_KEY = config.get("PROD_SECRET_KEY")