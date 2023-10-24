import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

from API.manager.menu_manager import MenuManager
from API.manager.restaurant_manager import RestaurantManager
from API.manager.token_manager import AccessTokenManager
from applibs.helpers import string_to_datetime


class AccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_token = models.TextField()
    access_token_init_time = models.CharField(max_length=100, null=True, blank=True)
    access_token_exp_time = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = AccessTokenManager()

    def update_access_token(self, parsed_response):
        self.access_token = parsed_response["access_token"]
        self.access_token_init_time = parsed_response["init_time"]
        self.access_token_exp_time = string_to_datetime(parsed_response["init_time"]) + timedelta(
            minutes=parsed_response["expires_in"])
        self.updated_at = timezone.now()
        self.save()


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = RestaurantManager()

    def __str__(self):
        return f"{self.name}-{self.location}"


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    menu = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = MenuManager()

