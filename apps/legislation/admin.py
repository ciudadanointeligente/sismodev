from django.contrib import admin
from .models import Law, LawAnalysis


@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ["title", "law_number", "jurisdiction", "status", "publication_date"]
    list_filter = ["status", "jurisdiction", "publication_date"]
    search_fields = ["title", "law_number", "summary"]


@admin.register(LawAnalysis)
class LawAnalysisAdmin(admin.ModelAdmin):
    list_display = ["law", "human_rights_score", "democratic_score", "analyzed_at"]
    list_filter = ["analyzed_at"]
