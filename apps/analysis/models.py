import uuid
from django.db import models


class HumanRightsParameter(models.Model):
    CATEGORY_CHOICES = [
        ("civil", "Civil"),
        ("political", "Político"),
        ("economic", "Económico"),
        ("social", "Social"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    weight = models.FloatField(default=1.0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parámetro de Derechos Humanos"
        verbose_name_plural = "Parámetros de Derechos Humanos"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class DemocraticParameter(models.Model):
    CATEGORY_CHOICES = [
        ("participation", "Participación"),
        ("accountability", "Rendición de cuentas"),
        ("transparency", "Transparencia"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    weight = models.FloatField(default=1.0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parámetro Democrático"
        verbose_name_plural = "Parámetros Democráticos"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class ContentAnalysis(models.Model):
    CONTENT_TYPES = [
        ("law", "Ley"),
        ("news", "Noticia"),
        ("event", "Evento"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.UUIDField()
    human_rights_score = models.FloatField(default=0)
    democratic_score = models.FloatField(default=0)
    violations_detected = models.JSONField(default=list, blank=True)
    concerns = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    llamaparse_response = models.JSONField(default=dict, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Análisis de Contenido"
        verbose_name_plural = "Análisis de Contenidos"
        ordering = ["-analyzed_at"]

    def __str__(self):
        return f"Análisis {self.content_type} {self.content_id}"
