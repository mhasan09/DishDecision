import base64
import json

from django.utils import timezone


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
