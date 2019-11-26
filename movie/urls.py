from django.urls import path
from . import views

# Connecting views.py and html files
urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('create/', views.create, name="create"),
]
