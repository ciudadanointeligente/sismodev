from rest_framework import serializers
from .models import LegislativeEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegislativeEvent
        fields = "__all__"
