from django.db import models

from applibs.helpers import get_three_consecutive_days
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

    def check_result(self, payload):
        try:
            data = self.filter(
                menu_id=payload["menu_id"],
                restaurant_id=payload["restaurant_id"],
            )

            three_days = get_three_consecutive_days()
            for days in three_days:
                if data.exists() in days:
                    return True
            return False

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None
