from django.urls import path
from .views import (
    AddMovieView, 
    MovieDetailView,
    MovieUpdateView,
    MovieDeleteView,
    MoviesListView,
    rate_movie
)


urlpatterns = [
    path('add/', AddMovieView.as_view(), name='add-movie'),
    path('<str:title>/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('<str:title>/<int:pk>/update/', MovieUpdateView.as_view(), name='update-movie'),
    path('<str:title>/<int:pk>/delete/', MovieDeleteView.as_view(), name='delete-movie'),
    path('all/', MoviesListView.as_view(), name='movies-list'),
    path('<str:title>/<int:pk>/rate/', rate_movie, name='rate-movie')
]