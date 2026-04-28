import uuid
from django.db import models


class Law(models.Model):
    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("published", "Publicado"),
        ("repealed", "Derogado"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    law_number = models.CharField(max_length=100, blank=True, db_index=True)
    jurisdiction = models.CharField(max_length=100, db_index=True)
    publication_date = models.DateField(null=True, blank=True, db_index=True)
    effective_date = models.DateField(null=True, blank=True)
    source_url = models.URLField(max_length=1000, blank=True)
    source_api = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published", db_index=True)
    category = models.CharField(max_length=100, blank=True, db_index=True)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ley"
        verbose_name_plural = "Leyes"
        ordering = ["-publication_date"]

    def __str__(self):
        return f"{self.law_number} - {self.title}"


class LawAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    law = models.OneToOneField(Law, on_delete=models.CASCADE, related_name="analysis")
    human_rights_score = models.FloatField(default=0)
    democratic_score = models.FloatField(default=0)
    concerns = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    llamaparse_response = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Análisis de Ley"
        verbose_name_plural = "Análisis de Leyes"
        ordering = ["-analyzed_at"]

    def __str__(self):
        return f"Análisis de {self.law.title}"
