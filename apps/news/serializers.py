from rest_framework import serializers
from .models import NewsArticle, NewsAnalysis


class NewsAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAnalysis
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    analysis = NewsAnalysisSerializer(read_only=True)

    class Meta:
        model = NewsArticle
        fields = "__all__"
