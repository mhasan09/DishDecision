from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class EmployeeManager(models.Manager):
    def save_employee(self, payload):
        try:
            return self.create(
                name=payload["name"],
                department=payload["department"],
                designation=payload["designation"],
            )

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

    def get_employee(self, employee_id):
        try:
            return self.get(id=employee_id)

        except ObjectDoesNotExist as e:
            logger.debug({"employee_id": employee_id, "db_exception_error": repr(e)})
            return None

        except Exception as e:
            logger.debug({"employee_id": employee_id, "db_exception_error": repr(e)})
            return None

