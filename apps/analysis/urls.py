from django.urls import path
from . import views

urlpatterns = [
    path("parse/", views.ParseDocumentView.as_view(), name="parse-document"),
    path("analyze/", views.AnalyzeContentView.as_view(), name="analyze-content"),
    path("parameters/", views.ParametersView.as_view(), name="parameters"),
]
