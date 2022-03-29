from django.db.models import Count, Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from backend.events.models import Event, UserEvent
from backend.events.serializers import EventDetailSerializer, UserEventSerializer

extend_events_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name='status', location=OpenApiParameter.QUERY,
            description='Event Status', required=False, type=str, enum=['past', 'pending']
        ),
    ],
)


class EventsAPIViewSet(ModelViewSet):
    serializer_class = EventDetailSerializer
    queryset = Event.objects

    def get_queryset(self):
        status = self.request.query_params.get('status')

        if status and status.lower() == 'past':
            queryset = self.queryset.filter(end_date__lte=timezone.now())
        elif status and status.lower() == 'pending':
            queryset = self.queryset.filter(end_date__gte=timezone.now())
        else:
            queryset = self.queryset.all()

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

    @extend_events_schema
    def list(self, request, *args, **kwargs):
        return super(EventsAPIViewSet, self).list(request, *args, **kwargs)

    @extend_events_schema
    def retrieve(self, request, *args, **kwargs):
        return super(EventsAPIViewSet, self).retrieve(request, *args, **kwargs)


class UserEventsAPIViewSet(ModelViewSet):
    serializer_class = UserEventSerializer
    queryset = UserEvent.objects.all()
