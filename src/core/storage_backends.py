from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


class DevMediaStorage(S3Boto3Storage):
    location = 'media_local'  # ajouter un nouveau fichier media_local/ sur S3
    file_overwrite = False
