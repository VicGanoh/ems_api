from .base import *
import os

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("HOST"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "PORT": os.environ.get("PORT"),
    }
}

SECRET_KEY = os.environ.get("SECRET_KEY")
