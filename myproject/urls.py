from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/queries/", include("queries.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/events/", include("events.urls")),
]
