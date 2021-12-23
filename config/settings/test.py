"""
With these settings, tests run faster.
"""
import logging
import os
import warnings

import requests

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="IbJd99K5fqq8fmvQpzXAtuR2vYDQwYReKAIt1yYVp5MIC8Y3XKLUgcA5cvf9SAxc",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

MEDIA_ROOT = os.path.join(APPS_DIR, "..", "test_media")  # noqa F405
STATIC_ROOT = os.path.join(APPS_DIR, "..", "test_public")  # noqa F405

REQUESTS_TIMEOUT = 0.01


# This is for informing when you forgot to mock the requests library.
class DummyRequests:
    """
    Mock requests class
    """

    pattern = 'unmocked call to address "{url}", with method "{method}"'

    def json(self):  # pylint: disable=R0201
        """
        raise an exception because we should specified it in cases where we use it
        """
        raise requests.RequestException

    def prep_to_call(self, method):
        """A call wrapper"""

        def inner(url, *args, **kwargs):
            """print out a warning message when we call unmocked API"""
            warnings.warn(self.pattern.format(method=method, url=url))
            return self

        return inner


requests.get = DummyRequests().prep_to_call("get")
requests.post = DummyRequests().prep_to_call("post")


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# This is because `django-log-request-id` was added.
logging.disable(logging.CRITICAL)
