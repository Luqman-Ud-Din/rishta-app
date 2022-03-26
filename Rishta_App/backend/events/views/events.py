from backend.events.models import Event
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from backend.events.serializers import EventDetailSerializer


class EventsAPIViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, id=pk)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)