from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import get_language

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from API.serializers import (
    AccessTokenSerializer,
    RefreshTokenSerializer,
)
from applibs.data_parser import data_parser

from applibs.jwt_utils import (
    get_access_token_data,
    decode_refresh_token,
)
from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class TokenAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = AccessTokenSerializer

    def __init__(self):
        super(TokenAPIView, self).__init__()
        self.language = "en"
        self.serializer_data = dict()
        self.user = None
        self.parsed_token_data = {}

    def check_regnum_user(self):
        check_if_user_exists = User.objects.filter(username__exact=self.serializer_data["username"]).last()
        if not check_if_user_exists:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return None

    def authenticate_regnum_user(self):
        self.user = authenticate(**self.serializer_data)
        if not self.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return None

    def generate_access_token(self):
        token_data = get_access_token_data(self.user)
        self.parsed_token_data = data_parser.render_token_data(token_data=token_data)
        logger.debug({"access_token_response": "success"})
        return None

    def process(self):
        if output := self.check_regnum_user():
            return output

        if output := self.authenticate_regnum_user():
            return output

        return self.generate_access_token()

    def post(self, request):
        self.language = get_language()
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.debug({"serializer_errors": repr(serializer.errors)})
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.serializer_data = serializer.data
        if output := self.process():
            return Response(output)

        return Response(data=self.parsed_token_data, status=status.HTTP_200_OK)


class RefreshTokenAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RefreshTokenSerializer

    def __init__(self):
        super(RefreshTokenAPIView, self).__init__()
        self.language = "en"
        self.serializer_data = dict()
        self.user_id = None
        self.user_obj = None
        self.parsed_token_data = {}

    def decode_regnum_refresh_token(self):
        self.user_id = decode_refresh_token(**self.serializer_data)
        if not self.user_id:
            return Response(status=status.HTTP_410_GONE)  # TODO: REFRESH_TOKEN_EXPIRED

        return None

    def check_regnum_user(self):
        self.user_obj = User.objects.filter(id=self.user_id).last()
        if not self.user_obj:
            return Response(status=status.HTTP_424_FAILED_DEPENDENCY)  # TODO: TOKEN_AUTH_FAILED

        return None

    def generate_new_token_by_refresh_token(self):
        token_data = get_access_token_data(self.user_obj)
        self.parsed_token_data = data_parser.render_token_data(token_data=token_data)
        logger.debug({"access_token_response": "success"})
        return None

    def process(self):
        if output := self.decode_regnum_refresh_token():
            return output
        if output := self.check_regnum_user():
            return output

        return self.generate_new_token_by_refresh_token()

    def post(self, request):
        self.language = get_language()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.debug({"serializer_errors": repr(serializer.errors)})
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.serializer_data = serializer.data
        if output := self.process():
            return Response(output)

        return Response(data=self.parsed_token_data, status=status.HTTP_200_OK)
