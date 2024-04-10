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

SECRET_KEY = "uku96+km&eq(wefr+@a!7nn09by_*!mc#)y)6g7uj)-t=3*8hjuku96+km&eq(wefr+@a!7nn09by_*!mc#)y)6g7uj)-t=3*8hj"