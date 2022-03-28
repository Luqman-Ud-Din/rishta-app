from django.utils import timezone
from backend.events.models import Event
from rest_framework.viewsets import ModelViewSet
from backend.events.serializers import EventDetailSerializer


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

        return queryset
