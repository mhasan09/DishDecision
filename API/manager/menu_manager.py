from django.db import models
from datetime import date
from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class MenuManager(models.Manager):
    def save_menu(self, payload):
        try:
            return self.create(
                restaurant=payload["id"],
                menu=payload["menu"],
            )

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

    def check_already_uploaded(self, payload):
        try:
            return self.filter(
                restaurant=payload["id"],
                created_at__day=date.today(),
            ).exists()

        except ObjectDoesNotExist as e:
            logger.debug({"restaurant_id": restaurant_id, "db_exception_error": repr(e)})
            return None

        except Exception as e:
            logger.debug({"restaurant_id": restaurant_id, "db_exception_error": repr(e)})
            return None