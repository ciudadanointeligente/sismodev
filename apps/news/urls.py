from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news-list"),
    path("<uuid:pk>/", views.NewsDetailView.as_view(), name="news-detail"),
    path("<uuid:pk>/analysis/", views.NewsAnalysisView.as_view(), name="news-analysis"),
    path("search/", views.NewsSearchView.as_view(), name="news-search"),
]
