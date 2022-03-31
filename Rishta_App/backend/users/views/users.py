from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from backend.events.enum import EventStatus
from backend.events.models import Event, UserEvent
from backend.events.serializers import EventDetailSerializer
from backend.users.models import User
from backend.users.serializers import UserDetailSerializer, UserBasicSerializer
from backend.users.tokens import account_activation_token


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        return obj == request.user


event_status_query_parameter = OpenApiParameter(
    name='status', location=OpenApiParameter.QUERY,
    description='Event Status', required=False, type=str, enum=[es.value for es in EventStatus]
)

event_interest_query_parameter = OpenApiParameter(
    name='interest', location=OpenApiParameter.QUERY,
    description='User Interest Status', required=False, type=str, enum=UserEvent.InterestStatus.values
)


class UserAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser | IsOwner)
    serializer_class = UserDetailSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_users_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        if self.action == 'get_events':
            return EventDetailSerializer
        elif self.action == 'list':
            return UserBasicSerializer

        return super(UserAPIViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.action == 'get_events':
            return self.get_user_events_queryset()

        return self.get_users_queryset()

    def get_users_queryset(self):
        return User.objects.all()

    def get_user_events_queryset(self):
        status = self.request.query_params.get('status')
        interest = self.request.query_params.get('interest')
        queryset = Event.objects.filter(user_events__user=self.get_object())

        if status and status.lower() == EventStatus.PAST.value:
            queryset = queryset.filter_past_events()
        elif status and status.lower() == EventStatus.PENDING.value:
            queryset = queryset.filter_pending_events()

        if interest:
            queryset = queryset.filter(user_events__interest_status=interest)

        return queryset.order_by('-end_date')

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

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Matrimony Account Activation Link.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    @extend_schema(
        responses=EventDetailSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name='id', location=OpenApiParameter.PATH,
                description='A unique integer value identifying this user.',
                required=True, type=int
            ),
            event_status_query_parameter,
            event_interest_query_parameter
        ],
    )
    @action(detail=True, methods=['get'], url_path='events')
    def get_events(self, request, *args, **kwargs):
        return super(UserAPIViewSet, self).list(request, *args, **kwargs)
