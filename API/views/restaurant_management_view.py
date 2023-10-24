from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from applibs.logging_utils import get_logger

from API.models import Restaurant
from API.serializers import CreateRestaurantSerializer

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
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        self.serializer_data = dict(serializer.validated_data)
        output = self.save_restaurant()
        return Response(output)
