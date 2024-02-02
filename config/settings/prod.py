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

AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = config.get("AWS_S3_SIGNATURE_NAME")
AWS_S3_REGION_NAME = config.get("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = config.get("DEFAULT_FILE_STORAGE")
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'