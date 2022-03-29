from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from backend.events.enum import EventStatus
from backend.events.models import Event, UserEvent
from backend.events.serializers import EventDetailSerializer, UserEventSerializer
from backend.users.serializers import UserBasicSerializer

User = get_user_model()

event_status_query_parameter = OpenApiParameter(
    name='status', location=OpenApiParameter.QUERY,
    description='Event Status', required=False, type=str, enum=[es.value for es in EventStatus]
)

event_interest_query_parameter = OpenApiParameter(
    name='interest', location=OpenApiParameter.QUERY,
    description='User Interest Status', required=False, type=str, enum=UserEvent.InterestStatus.values
)

extend_events_schema = extend_schema(
    parameters=[event_status_query_parameter],
)


class EventsAPIViewSet(ModelViewSet):
    serializer_class = EventDetailSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_events_queryset())

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
        if self.action == 'get_users':
            return UserBasicSerializer

        return super(EventsAPIViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.action == 'get_users':
            return self.get_event_users_queryset()

        return self.get_events_queryset()

    def get_events_queryset(self):
        status = self.request.query_params.get('status')
        queryset = Event.objects

        if status and status.lower() == EventStatus.PAST.value:
            queryset = queryset.filter_past_events()
        elif status and status.lower() == EventStatus.PENDING.value:
            queryset = queryset.filter_pending_events()
        else:
            queryset = queryset.all()

        queryset = queryset.annotate(
            attend_count=Count(
                'user_events',
                filter=Q(user_events__interest_status=UserEvent.InterestStatus.ATTEND)
            ),
            not_attend_count=Count(
                'user_events',
                filter=Q(user_events__interest_status=UserEvent.InterestStatus.NOT_ATTEND)
            ),
            ignore_count=Count(
                'user_events',
                filter=Q(user_events__interest_status=UserEvent.InterestStatus.IGNORE)
            )
        ).order_by('-start_date')

        return queryset

    def get_event_users_queryset(self):
        interest = self.request.query_params.get('interest')
        queryset = User.objects.filter(
            user_events__event=self.get_object(),
        )

        if interest:
            queryset = queryset.filter(user_events__interest_status=interest)

        return queryset.order_by('created_at')

    @extend_events_schema
    def list(self, request, *args, **kwargs):
        return super(EventsAPIViewSet, self).list(request, *args, **kwargs)

    @extend_events_schema
    def retrieve(self, request, *args, **kwargs):
        return super(EventsAPIViewSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=UserBasicSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name='id', location=OpenApiParameter.PATH,
                description='A unique integer value identifying this event.',
                required=True, type=int
            ),
            event_status_query_parameter,
            event_interest_query_parameter
        ],
    )
    @action(detail=True, methods=['get'], url_path='users')
    def get_users(self, request, *args, **kwargs):
        return super(EventsAPIViewSet, self).list(request, *args, **kwargs)


class UserEventsAPIViewSet(ModelViewSet):
    serializer_class = UserEventSerializer
    queryset = UserEvent.objects.all()
