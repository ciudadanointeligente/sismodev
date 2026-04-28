from rest_framework import serializers
from .models import Law, LawAnalysis


class LawAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawAnalysis
        fields = "__all__"


class LawSerializer(serializers.ModelSerializer):
    analysis = LawAnalysisSerializer(read_only=True)

    class Meta:
        model = Law
        fields = "__all__"
