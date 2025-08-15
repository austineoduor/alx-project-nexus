from django.urls import path
from .views import (RegisterView,
                    FavoriteMovieListCreateView,
                    AddFavoriteMovieView,
                    FavoriteMovieDeleteView,
                    FavoriteMovieListView,
                    RateMovieView,
                    RecentlyAddedFavoritesView,
                    RecentlyRemovedFavoritesView,
                    WatchlistRemoveView,
                    WatchlistView
                    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    #movie rating
    path('movies/rate/', RateMovieView.as_view(), name='rate-movie'),

    #watch list
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/create/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>', WatchlistRemoveView.as_view(), name='watchlist-remove'),
    
    # Favorites
    path('favorites/', FavoriteMovieListView.as_view(), name="favorite-movie-list"),
    path('favorites/create/', FavoriteMovieListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/add/', AddFavoriteMovieView.as_view(), name="favorite-add"),
    path('favorites/<int:movie_id>', FavoriteMovieDeleteView.as_view(), name='favorite-delete'),
    path("favorites/recently-added/", RecentlyAddedFavoritesView.as_view(), name="recently-added-favorites"),
    path("favorites/recently-removed/", RecentlyRemovedFavoritesView.as_view(), name="recently-removed-favorites"),
]