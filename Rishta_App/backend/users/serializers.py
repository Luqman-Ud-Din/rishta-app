from rest_framework import serializers

from backend.users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
        exclude = [
            'password', 'last_login',
            'groups', 'user_permissions',
            'date_joined'
        ]
