from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import date
from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class MenuManager(models.Manager):
    def upload_menu(self, payload):
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
                created_at__day=date.today().day,
            ).exists()

        except ObjectDoesNotExist as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

    def get_menu_for_today(self):
        try:
            return list(self.filter(
                created_at__day=date.today().day
            ).values(
                "menu",
                "restaurant__name",
                "restaurant__location"
            ))

        except Exception as e:
            logger.debug(repr(e))
            return None

    def get_eligible_menu_for_vote(self):
        try:
            return self.filter(
                created_at__day=date.today().day
            ).exists()

        except Exception as e:
            logger.debug(repr(e))
            return None

    def prepare_menu_vote(self, menu_id):
        try:
            return self.get(id=menu_id)

        except ObjectDoesNotExist as e:
            logger.debug({"menu_id": menu_id, "db_exception_error": repr(e)})
            return None

        except Exception as e:
            logger.debug({"menu_id": menu_id, "db_exception_error": repr(e)})
            return None
