from django.urls import path
from .views import (RegisterView,
                    FavoriteMovieListCreateView,
                    AddFavoriteMovieView,
                    FavoriteMovieDeleteView,
                    FavoriteMovieListView,
                    RateMovieView
                    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    #movie rating
    path('movies/rate/', RateMovieView.as_view(), name='rate-movie'),

    # Favorites
    path('favorites/', FavoriteMovieListView.as_view(), name="favorite-movie-list"),
    path('favorites/create/', FavoriteMovieListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/add/', AddFavoriteMovieView.as_view(), name="favorite-add"),
    path('favorites/<int:movie_id>/', FavoriteMovieDeleteView.as_view(), name='favorite-delete'),
]