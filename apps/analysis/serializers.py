from rest_framework import serializers
from .models import HumanRightsParameter, DemocraticParameter, ContentAnalysis


class HumanRightsParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanRightsParameter
        fields = "__all__"


class DemocraticParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemocraticParameter
        fields = "__all__"


class ParameterSerializer(serializers.Serializer):
    pass


class ContentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentAnalysis
        fields = "__all__"
