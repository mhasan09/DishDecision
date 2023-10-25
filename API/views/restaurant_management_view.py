from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from applibs.helpers import check_time_limit_validity_for_uploading_menu
from applibs.logging_utils import get_logger

from API.models import Restaurant, Menu
from API.serializers import (
    CreateRestaurantSerializer,
    UploadMenuSerializer,
)

logger = get_logger(__name__)


class CreateRestaurantAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(CreateRestaurantAPIView, self).__init__()
        self.request = None
        self.serializer_data = dict()
        self.serializer_class = CreateRestaurantSerializer

    def save_restaurant(self):
        registration_obj = Restaurant.objects.save_restaurant(payload=self.serializer_data)
        if registration_obj:
            return status.HTTP_201_CREATED

        return status.HTTP_424_FAILED_DEPENDENCY

    def post(self, request):
        self.request = request
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            logger.debug({"serializer_error": repr(serializer.errors)})
            return Response("Invalid data format", status=status.HTTP_406_NOT_ACCEPTABLE)

        self.serializer_data = dict(serializer.validated_data)
        output = self.save_restaurant()
        return Response(output)


class UploadMenuAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(UploadMenuAPIView, self).__init__()
        self.request = None
        self.serializer_data = dict()
        self.serializer_class = UploadMenuSerializer
        self.restaurant_obj = None

    def check_upload_validity(self):
        self.restaurant_obj = Restaurant.objects.get_restaurant(restaurant_id=self.serializer_data["id"])
        if not self.restaurant_obj:
            return status.HTTP_404_NOT_FOUND

        self.serializer_data["id"] = self.restaurant_obj
        if Menu.objects.check_already_uploaded(payload=self.serializer_data):
            return status.HTTP_406_NOT_ACCEPTABLE

        time_validity = check_time_limit_validity_for_uploading_menu()
        if time_validity:
            self.upload_menu()
        return status.HTTP_406_NOT_ACCEPTABLE

    def upload_menu(self):
        uploaded = Menu.objects.upload_menu(payload=self.serializer_data)
        if uploaded:
            return status.HTTP_201_CREATED
        return status.HTTP_424_FAILED_DEPENDENCY

    def post(self, request):
        self.request = request
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            logger.debug({"serializer_error": repr(serializer.errors)})
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        self.serializer_data = dict(serializer.validated_data)
        output = self.check_upload_validity()
        return Response(output)


class GetMenuAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_menu_for_today():
        return Menu.objects.get_menu_for_today()

    def get(self, request):
        output = self.get_menu_for_today()
        return Response(output)
