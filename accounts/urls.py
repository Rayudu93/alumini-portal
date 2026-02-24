from django.urls import path
from .views import LoginView, SignupView, StudentProfileView, AlumniProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("student/profile/", StudentProfileView.as_view()),
    path("alumni/profile/", AlumniProfileView.as_view()),
]
