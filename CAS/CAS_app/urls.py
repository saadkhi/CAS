from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),  # Main view of the CAS application

    path("reload/", views.home_view, name="browser_reload"),  # Browser reload endpoint for development
]