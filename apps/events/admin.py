from django.contrib import admin
from .models import LegislativeEvent


@admin.register(LegislativeEvent)
class LegislativeEventAdmin(admin.ModelAdmin):
    list_display = ["title", "event_type", "date", "location"]
    list_filter = ["event_type", "date"]
    search_fields = ["title", "description"]
