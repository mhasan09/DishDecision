from django.urls import path

from API.views.token_view import (
    TokenAPIView,
    RefreshTokenAPIView,
)

urlpatterns = [
    path("service/v1/auth/token/", TokenAPIView.as_view(), name="access-token"),
    path("service/v1/auth/token-refresh/", RefreshTokenAPIView.as_view(), name="access-by-refresh-token"),
]
