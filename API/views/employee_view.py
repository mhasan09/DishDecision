from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from applibs.logging_utils import get_logger

from API.models import Employee
from API.serializers import CreateEmployeeSerializer

logger = get_logger(__name__)


class CreateEmployeeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(CreateEmployeeAPIView, self).__init__()
        self.request = None
        self.serializer_data = dict()
        self.serializer_class = CreateEmployeeSerializer

    def save_employee(self):
        employee_obj = Employee.objects.save_employee(payload=self.serializer_data)
        if employee_obj:
            return status.HTTP_201_CREATED

        return status.HTTP_424_FAILED_DEPENDENCY

    def post(self, request):
        self.request = request
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            logger.debug({"serializer_error": repr(serializer.errors)})
            return Response("Invalid data format", status=status.HTTP_406_NOT_ACCEPTABLE)

        self.serializer_data = dict(serializer.validated_data)
        output = self.save_employee()
        return Response(output)

