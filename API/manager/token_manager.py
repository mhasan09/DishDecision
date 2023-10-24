from django.db import models
from django.utils import timezone
from datetime import timedelta

from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class AccessTokenManager(models.Manager):
    def clean_tokens(self):
        return self.first().delete()

    def save_access_token(self, response):
        try:
            return self.create(
                access_token=response["access_token"],
                access_token_init_time=timezone.now(),
                access_token_exp_time=timezone.now() + timedelta(seconds=response["expires_in"]),
            )
        except Exception as e:
            logger.debug({"db_exception_errors": repr(e)})
            return None
