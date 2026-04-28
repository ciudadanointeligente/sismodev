from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventListView.as_view(), name="event-list"),
    path("<uuid:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("calendar/", views.EventCalendarView.as_view(), name="event-calendar"),
]
