from django.urls import path

from . import views
from .views import LoginView, SignupView, ProfileView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(), name="login"),
    path("signup", SignupView.as_view(), name="signup"),
    path("profile", ProfileView.as_view(), name="profile")
]