import uuid
from django.db import models


class LegislativeEvent(models.Model):
    EVENT_TYPES = [
        ("vote", "Votación"),
        ("hearing", "Audiencia"),
        ("committee", "Comité"),
        ("debate", "Debate"),
        ("other", "Otro"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default="other", db_index=True)
    date = models.DateTimeField(db_index=True)
    location = models.CharField(max_length=300, blank=True)
    participants = models.JSONField(default=list, blank=True)
    outcome = models.TextField(blank=True)
    source_url = models.URLField(max_length=1000, blank=True)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento Legislativo"
        verbose_name_plural = "Eventos Legislativos"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"
