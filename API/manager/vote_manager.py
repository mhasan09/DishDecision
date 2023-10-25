from django.db import models
from datetime import date
from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class VoteManager(models.Manager):
    def cast_vote(self, payload):
        try:
            return self.create(
                voter_id=payload["voter_id"],
                vote_for=payload["vote_for"],
            )

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None

    def check_voter(self, payload):
        try:
            return self.filter(
                voter_id=payload["voter_id"],
                created_at__day=date.today().day,
            ).exists()

        except Exception as e:
            logger.debug({"payload": payload, "db_exception_error": repr(e)})
            return None
