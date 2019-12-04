from django.urls import path
from . import views

# Connecting views.py and html files
urlpatterns = [
    # Connects the homepage front-end and backend
    path('', views.home_page, name="home_page"),
    # connects the create form front-end to backend
    path('create/', views.create, name="create"),
    # connects edit form. for th url it puts the movie_id that the user chose and turns it into a string to be displayed
    path('edit/<str:movie_id>', views.edit, name="edit"),
    # connects delete button. same as edit path but for delete
    path('delete/<str:movie_id>', views.delete, name="delete"),
]
