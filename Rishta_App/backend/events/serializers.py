from rest_framework import serializers

from backend.events.models import Event


class EventDetailSerializer(serializers.Serializer):
    class Meta:
        model = Event
        fields = '__all__'
