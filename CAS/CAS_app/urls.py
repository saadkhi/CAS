from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),  # Main view of the CAS application
    path("resume-advisor/", views.resume_advisor_view, name="resume_advisor_view"),  # Resume advisor view

    path("reload/", views.home_view, name="browser_reload"),  # Browser reload endpoint for development
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]