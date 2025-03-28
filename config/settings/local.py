from .base import *
import os

from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER"),
        "HOST": os.getenv("HOST"),
        "PASSWORD": os.getenv("DB_PASS"),
        "PORT": os.getenv("PORT"),
    }
}

SECRET_KEY = os.getenv("SECRET_KEY")
