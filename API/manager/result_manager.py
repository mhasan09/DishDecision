from django.db import models

from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class ResultManager(models.Manager):
    def save_result(self, payload):
        try:
            return self.create(
                menu_id=payload["menu_id"],
                restaurant_id=payload["restaurant_id"],
            )

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None
