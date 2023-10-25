from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from applibs.helpers import check_time_limit_validity_for_uploading_menu
from applibs.logging_utils import get_logger

from API.models import Restaurant, Menu, Vote, Result
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
        # check if the restaurant is in the system
        self.restaurant_obj = Restaurant.objects.get_restaurant(restaurant_id=self.serializer_data["id"])
        if not self.restaurant_obj:
            return status.HTTP_404_NOT_FOUND

        self.serializer_data["id"] = self.restaurant_obj

        # check if the restaurant has already uploaded today's menu
        if Menu.objects.check_already_uploaded(payload=self.serializer_data):
            return status.HTTP_406_NOT_ACCEPTABLE

        # check if the menu has been uploaded in the required time period
        time_validity = check_time_limit_validity_for_uploading_menu()
        if time_validity:
            self.upload_menu()
            return status.HTTP_201_CREATED

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


class GetWinnerAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(GetWinnerAPIView, self).__init__()
        self.request = None
        self.response_data = dict()

    def preprocess_winner_data(self):
        self.response_data = Vote.objects.get_winner()
        if len(self.response_data) != 0:
            winner_data = max(self.response_data, key=lambda d: d['total_vote_count'])
            self.save_result(winner_data=winner_data)
            menu_name = Menu.objects.get(id=winner_data["vote_for"]).menu
            restaurant_name = Menu.objects.get(id=winner_data["vote_for"]).restaurant.name
            location = Menu.objects.get(id=winner_data["vote_for"]).restaurant.location
            return self.set_response(menu_name, restaurant_name, location)
        return status.HTTP_406_NOT_ACCEPTABLE


    @staticmethod
    def save_result(winner_data):
        menu_id = Menu.objects.get(id=winner_data["vote_for"])
        restaurant_id = Menu.objects.get(id=winner_data["vote_for"]).restaurant
        payload = dict()
        payload["menu_id"] = menu_id
        payload["restaurant_id"] = restaurant_id
        result_saved = Result.objects.save_result(payload=payload)
        if result_saved:
            return None

    @staticmethod
    def set_response(*args):
        return {
            "menu": args[0],
            "restaurant": args[1],
            "location": args[2],
        }

    def get(self, request):
        output = self.preprocess_winner_data()
        return Response(output)
