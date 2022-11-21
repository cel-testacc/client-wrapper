from django.urls import path
from django.views.generic import TemplateView
from .views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
