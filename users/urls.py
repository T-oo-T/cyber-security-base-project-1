from django.urls import path

from . import views
from .views import LoginView, SignupView, ProfileView, LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("profile/<int:user_id>", ProfileView.as_view(), name="profile")
]