import uuid
from django.db import models


class NewsArticle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    source = models.CharField(max_length=200, db_index=True)
    source_url = models.URLField(max_length=1000, blank=True)
    author = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    country = models.CharField(max_length=10, db_index=True)
    tags = models.JSONField(default=list, blank=True)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artículo de Noticias"
        verbose_name_plural = "Artículos de Noticias"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} - {self.source}"


class NewsAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.OneToOneField(NewsArticle, on_delete=models.CASCADE, related_name="analysis")
    human_rights_impact = models.FloatField(default=0)
    democratic_impact = models.FloatField(default=0)
    sentiment = models.CharField(max_length=50, blank=True)
    key_concerns = models.JSONField(default=list, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    llamaparse_response = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Análisis de Noticias"
        verbose_name_plural = "Análisis de Noticias"
        ordering = ["-analyzed_at"]

    def __str__(self):
        return f"Análisis de {self.article.title}"
