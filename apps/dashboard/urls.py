from django.urls import path
from . import views

urlpatterns = [
    path("summary/", views.DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("human-rights/", views.HumanRightsMetricsView.as_view(), name="human-rights-metrics"),
    path("democratic/", views.DemocraticMetricsView.as_view(), name="democratic-metrics"),
]
