from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from applibs.helpers import check_time_limit_validity_for_voting
from applibs.logging_utils import get_logger

from API.models import Employee, Menu, Vote
from API.serializers import CreateEmployeeSerializer, CastVoteSerializer

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


class CastVoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(CastVoteAPIView, self).__init__()
        self.request = None
        self.serializer_data = dict()
        self.serializer_class = CastVoteSerializer
        self.voter_obj = None
        self.vote_obj = None
        self.voter_eligible_payload = dict()

    def check_voting_eligibility(self):
        self.voter_obj = Employee.objects.get_employee(employee_id=self.serializer_data["voter_id"])

        self.voter_eligible_payload["voter_id"] = self.voter_obj
        voter_already_voted = Vote.objects.check_voter(payload=self.voter_eligible_payload)

        if voter_already_voted:
            return status.HTTP_406_NOT_ACCEPTABLE

        if not self.voter_obj:
            return status.HTTP_406_NOT_ACCEPTABLE

        time_validity = check_time_limit_validity_for_voting()
        if time_validity:
            is_vote_acceptable = Menu.objects.get_eligible_menu_for_vote()
            if is_vote_acceptable:
                self.preprocess_vote()
                return status.HTTP_201_CREATED
            else:
                return status.HTTP_406_NOT_ACCEPTABLE

        return status.HTTP_406_NOT_ACCEPTABLE

    def preprocess_vote(self):
        self.vote_obj = Menu.objects.prepare_menu_vote(menu_id=self.serializer_data["vote_for"])
        if self.vote_obj:
            self.cast_vote()
            return None

        return status.HTTP_424_FAILED_DEPENDENCY

    def cast_vote(self):
        self.serializer_data["voter_id"] = self.voter_obj
        self.serializer_data["vote_for"] = self.vote_obj
        vote_casted = Vote.objects.cast_vote(payload=self.serializer_data)
        if vote_casted:
            return None
        return status.HTTP_424_FAILED_DEPENDENCY

    def post(self, request):
        self.request = request
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            logger.debug({"serializer_error": repr(serializer.errors)})
            return Response("Invalid data format", status=status.HTTP_406_NOT_ACCEPTABLE)

        self.serializer_data = dict(serializer.validated_data)
        output = self.check_voting_eligibility()
        return Response(output)
