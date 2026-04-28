from django.contrib import admin
from .models import NewsArticle, NewsAnalysis


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "source", "country", "published_at"]
    list_filter = ["source", "country", "published_at"]
    search_fields = ["title", "content"]


@admin.register(NewsAnalysis)
class NewsAnalysisAdmin(admin.ModelAdmin):
    list_display = ["article", "human_rights_impact", "democratic_impact", "analyzed_at"]
    list_filter = ["analyzed_at"]
