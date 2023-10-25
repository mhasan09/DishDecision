from django.urls import path

from API.views.token_view import (
    TokenAPIView,
    RefreshTokenAPIView,
)
from API.views.restaurant_management_view import CreateRestaurantAPIView, UploadMenuAPIView, GetMenuAPIView, GetWinnerAPIView
from API.views.employee_view import CreateEmployeeAPIView, CastVoteAPIView

urlpatterns = [
    path("v1/auth/token/", TokenAPIView.as_view(), name="access-token"),
    path("v1/auth/token-refresh/", RefreshTokenAPIView.as_view(), name="access-by-refresh-token"),
    path("v1/create-restaurant/", CreateRestaurantAPIView.as_view(), name="create-restaurant"),
    path("v1/upload-menu/", UploadMenuAPIView.as_view(), name="upload-menu"),
    path("v1/create-employee/", CreateEmployeeAPIView.as_view(), name="create-employee"),
    path("v1/get-menu/", GetMenuAPIView.as_view(), name="get-menu"),
    path("v1/cast-vote/", CastVoteAPIView.as_view(), name="cast-vote"),
    path("v1/get-winner/", GetWinnerAPIView.as_view(), name="get-winner"),
]
