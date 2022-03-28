from django.utils import timezone
from backend.events.models import Event
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from backend.events.serializers import EventDetailSerializer


class EventsAPIViewSet(ModelViewSet):
    serializer_class = EventDetailSerializer
    queryset = Event.objects.all()

    def list(self, request):
        status = self.request.query_params.get('status')

        if status and status.lower() == 'past':
            queryset = self.queryset.filter(end_date__lte=timezone.now())
        elif status and status.lower() == 'pending':
            queryset = self.queryset.filter(end_date__gte=timezone.now())
        else:
            queryset = self.queryset
        if not queryset:
            return Response([])

        serializer = EventDetailSerializer(queryset.order_by('start_date'), many=True)
        return Response(serializer.data) 

    def retrieve(self, request, pk=None):
        event = get_object_or_404(self.queryset, id=pk)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)