from django.urls import path
from .views import TrendingMoviesView, RecommendedMoviesView

urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('recommended/<int:movie_id>/', RecommendedMoviesView.as_view(), name='recommended-movies'),
]