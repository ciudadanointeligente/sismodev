from django.contrib import admin
from .models import HumanRightsParameter, DemocraticParameter, ContentAnalysis


@admin.register(HumanRightsParameter)
class HumanRightsParameterAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "weight", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]


@admin.register(DemocraticParameter)
class DemocraticParameterAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "weight", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]


@admin.register(ContentAnalysis)
class ContentAnalysisAdmin(admin.ModelAdmin):
    list_display = ["content_type", "content_id", "human_rights_score", "democratic_score", "analyzed_at"]
    list_filter = ["content_type", "analyzed_at"]
