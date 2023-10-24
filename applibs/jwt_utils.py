import base64
import json
import jwt

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from DishDecision.settings import SIMPLE_JWT, SECRET_KEY
from applibs.logging_utils import get_logger

logger = get_logger(__name__)

def decode_field_from_jwt(token: str, field: str):
    if not token:
        return ""

    token_parts = token.split(".")

    if len(token_parts) != 3:
        return ""

    token_mid = token_parts[1]

    # fix padding
    token_mid = token_mid + "=" * (len(token_mid) % 4)

    token_mid_decoded = base64.b64decode(token_mid)
    token_mid_data = json.loads(token_mid_decoded)

    return token_mid_data.get(field, "")


def decode_jti(token):
    return decode_field_from_jwt(token, "jti")


def decode_exp(token):
    exp = decode_field_from_jwt(token, "exp")
    if not exp:
        return 0
    return int(exp)


def is_jwt_token_valid(token, expiry_threshold=0):
    exp = decode_exp(token)

    # adjust exp time with threshold
    exp = exp - expiry_threshold
    now = timezone.now().timestamp()

    return now < exp

def get_access_token_data(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    output = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "access_token_expiry_time": SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME"),
        "refresh_token_expiry_time": SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME")
    }

    return output


def decode_refresh_token(refresh_token) -> dict:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]

    except Exception as e:
        logger.error(repr(e))
        return None
