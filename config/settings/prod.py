from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = ["*"]

if os.getenv("DEBUG") == "False":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "HOST": os.getenv("HOST"),
            "PASSWORD": os.getenv("DB_PASS"),
            "PORT": os.getenv("PORT"),
        }
    }

SECRET_KEY = os.getenv("SECRET_KEY")
