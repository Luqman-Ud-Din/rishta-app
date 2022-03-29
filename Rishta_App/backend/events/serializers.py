from rest_framework import serializers

from backend.events.models import Event, UserEvent


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    attend_count = serializers.SerializerMethodField()
    not_attend_count = serializers.SerializerMethodField()
    ignore_count = serializers.SerializerMethodField()

    def get_attend_count(self, obj):
        return getattr(obj, 'attend_count', None)

    def get_not_attend_count(self, obj):
        return getattr(obj, 'not_attend_count', None)

    def get_ignore_count(self, obj):
        return getattr(obj, 'ignore_count', None)


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
