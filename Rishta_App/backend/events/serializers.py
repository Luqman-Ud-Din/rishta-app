from rest_framework import serializers

from backend.events.models import Event


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
