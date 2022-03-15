from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.users.models import User
from backend.users.serializers import UserDetailSerializer, UserBasicSerializer
from backend.users.tokens import account_activation_token


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    authqueryset = TwoFactorAuth.objects.all()

    def get_serializer_class(self):
        return UserBasicSerializer if self.action == 'list' else super(UserAPIViewSet, self).get_serializer_class()

    def is_create_api(self):
        return self.action == 'create'

    def get_permissions(self):
        if self.is_create_api():
            return [AllowAny()]
        return super(UserAPIViewSet, self).get_permissions()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):  # optional
            request.data._mutable = True

        request.data.update({'is_active': False})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        self.send_activation_email(request, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def generate_token_and_store(self, user):
        auth_token = account_activation_token.make_token(user)
        two_factor_row = TwoFactorAuth(user=user, auth_token=auth_token)
        two_factor_row.save()
        return auth_token

    def send_activation_email(self, request, user):
        auth_token = generate_token_and_store(user)
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': auth_token,
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
