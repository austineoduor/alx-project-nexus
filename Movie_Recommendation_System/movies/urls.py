from django.urls import path
from .views import TrendingMoviesView, RecommendedMoviesView

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path("movies/recommended/", RecommendedMoviesView.as_view(), name="recommended_movies"),
    path('movies/recommended/<int:movie_id>/', RecommendedMoviesView.as_view(), name='recommended-movies'),
]