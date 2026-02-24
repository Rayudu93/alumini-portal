# events/serializers.py
from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    total_registrations = serializers.IntegerField(
        source="registered_users.count",
        read_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "created_by",
            "total_registrations",
        ]
        read_only_fields = ["created_by"]
