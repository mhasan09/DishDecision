import logging

from django.conf import settings


def get_logger(name):
    return logging.getLogger(f"{settings.LOGGER_ROOT_NAME}.{name}")
