from pickle import FALSE
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwtSerilizer
from rest_framework_simplejwt.settings import api_settings

from backend.users.tokens import OTP
from backend.users.models import User, OTP as otp_model


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar',
            'first_name', 'last_name', 'password',
            'gender', 'religion', 'blood_group'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'avatar': {'read_only': True},
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


class CustomeTokenObtainPairSerializer(jwtSerilizer.TokenObtainSerializer):
    @classmethod
    def get_token(cls):
        return OTP.generate_token()

    def store_otp(self, attrs, otp):
        otp_row = otp_model(user_id=attrs['userid'], otp_token=otp)
        otp_row.save()
        return True
    
    def send_otp_email(self, user, otp):
        mail_subject = 'OTP for login!'
        message = render_to_string('otp_email.html', {
            'user': user,
            'token': otp
        })
        to_email = user['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        try:
            email.send()
            return True
        except:
            return False

    def validate(self, attrs):
        attrs['userid'] = 2
        attrs['email'] = 'fahadshawal@gmail.com'
        
        super().validate(attrs)
        otp = self.get_token()
        self.store_otp(attrs, otp)
        self.send_otp_email(attrs, otp)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return True
