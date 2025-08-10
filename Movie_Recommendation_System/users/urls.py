from django.urls import path
from .views import RegisterView, FavoriteMovieListCreateView, FavoriteMovieDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('favorites/', FavoriteMovieListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:movie_id>/', FavoriteMovieDeleteView.as_view(), name='favorite-delete'),
]