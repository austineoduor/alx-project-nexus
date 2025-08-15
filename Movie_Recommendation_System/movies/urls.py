from django.urls import path
from .views import (TrendingMoviesView,
                    RecommendedMoviesView,
                    MovieListCreateView,
                    ClearCacheView)

urlpatterns = [
    path('', MovieListCreateView.as_view(), name='movie-list'),
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('recommended/', RecommendedMoviesView.as_view(), name="recommended_movies"),
    path('recommended/<int:movie_id>/', RecommendedMoviesView.as_view(), name='recommended-movie'),
    path('cache/clear/', ClearCacheView.as_view(), name='clear-cache'),
]