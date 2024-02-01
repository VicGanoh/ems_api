from .base import *
from dotenv import dotenv_values
import dj_database_url

config = dotenv_values(".env")

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.get("DB_NAME_PROD"),
        "USER": config.get("USER_PROD"),
        "HOST": config.get("HOST_PROD"),
        "PASSWORD": config.get("DB_PASS_PROD"),
        "PORT": config.get("PORT"),
    }
}

SECRET_KEY = config.get("PROD_SECRET_KEY")