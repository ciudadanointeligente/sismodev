from django.urls import path
from . import views

urlpatterns = [
    path("", views.LawListView.as_view(), name="law-list"),
    path("<uuid:pk>/", views.LawDetailView.as_view(), name="law-detail"),
    path("<uuid:pk>/analysis/", views.LawAnalysisView.as_view(), name="law-analysis"),
    path("search/", views.LawSearchView.as_view(), name="law-search"),
    path("<uuid:pk>/reanalyze/", views.LawReanalyzeView.as_view(), name="law-reanalyze"),
]
