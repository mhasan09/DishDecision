from rest_framework import serializers


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)


class CreateRestaurantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    location = serializers.CharField(max_length=20)


class UploadMenuSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=55)
    menu = serializers.CharField(max_length=255)