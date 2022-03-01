from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from backend.users.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name', 'password',
            'gender', 'religion', 'blood_group'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    @transaction.atomic
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserBasicSerializer, self).create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        if 'avatar' in validated_data and not validated_data['avatar']:
            del validated_data['avatar']

        return super(UserBasicSerializer, self).update(instance, validated_data)


class UserDetailSerializer(UserBasicSerializer):
    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'created_at',
            'updated_at', 'date_joined', 'is_active',
            'is_staff', 'is_superuser', 'last_login',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'id': {'read_only': True}
        }
