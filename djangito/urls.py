from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/laws/", include("apps.legislation.urls")),
    path("api/v1/news/", include("apps.news.urls")),
    path("api/v1/events/", include("apps.events.urls")),
    path("api/v1/analysis/", include("apps.analysis.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]
