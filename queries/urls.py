# queries/urls.py
from django.urls import path
from .views import (
    CreateQueryView,
    AcceptQueryView,
    AnswerQueryView,
    QueryListView,
)

urlpatterns = [
    path("create/", CreateQueryView.as_view()),
    path("list/", QueryListView.as_view()),
    path("accept/<int:query_id>/", AcceptQueryView.as_view()),
    path("answer/<str:query_id>/", AnswerQueryView.as_view()),
]
