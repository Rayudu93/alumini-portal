# events/urls.py
from django.urls import path
from .views import (
    CreateEventView,
    EventListView,
    RegisterEventView,
    MyRegisteredEventsView,
)

urlpatterns = [
    path("create/", CreateEventView.as_view()),
    path("list/", EventListView.as_view()),
    path("register/<int:event_id>/", RegisterEventView.as_view()),
    path("my-registrations/", MyRegisteredEventsView.as_view()),
]
