from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class RestaurantManager(models.Manager):
    def save_restaurant(self, payload):
        try:
            return self.create(
                name=payload["name"],
                location=payload["location"],
            )

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

    def get_restaurant(self, restaurant_id):
        try:
            return self.get(id=restaurant_id)

        except ObjectDoesNotExist as e:
            logger.debug({"restaurant_id": restaurant_id, "db_exception_error": repr(e)})
            return None

        except Exception as e:
            logger.debug({"restaurant_id": restaurant_id, "db_exception_error": repr(e)})
            return None

