from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


# https://github.com/ckz8780/boutique_ado_v1/blob/250e2c2b8e43cccb56b4721cd8a8bd4de6686546/custom_storages.py