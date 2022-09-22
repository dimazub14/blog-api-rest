from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    """
    S3 static storage.
    """

    location = "static"
    default_acl = None


class MediaRootS3Boto3Storage(S3Boto3Storage):
    """
    S3 media storage.
    """

    location = "media"
    file_overwrite = False


class PrivateMediaRootS3Boto3Storage(S3Boto3Storage):
    """
    Private S3 media storage.
    """

    location = "private"
    default_acl = "private"
    file_overwrite = True
    custom_domain = False
    querystring_auth = True
