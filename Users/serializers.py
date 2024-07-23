from rest_framework import serializers
from .models import *


class Users_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = "__all__"

    def validate_phone_number(self, value):
        print(len(value))
        if len(value) > 10 or len(value) < 10:
            raise serializers.ValidationError(
                'Phone numberz must have 10 character')
        if value[0] != "0":
            raise serializers.ValidationError('Phone number must start with 0')
        return value

    def validate_password(self, value):
        if len(value) < 4:
            raise serializers.ValidationError(
                "password must contain atleast 4 characters")
        return value

    def create(self, validate_data):
        password = validate_data.pop('password')
        user = Users.objects.create_user(password=password, **validate_data)
        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError("New password don't match")
        return data

    class Meta:
        model = Users
        fields = ['old_password', 'new_password', 'confirm_new_password']
