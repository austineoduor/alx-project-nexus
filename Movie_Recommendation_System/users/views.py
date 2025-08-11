from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FavoriteMovie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, AddFavoriteSerializer, FavoriteMovieSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    Requires: username, email, password.
    Returns the created user object.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user account.",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    swagger_schema_fields = {
        "example": {
            "username": "john_doe",
            "password": "securepassword123"
        }
    }

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Obtain a JWT access and refresh token using username and password.",
        tags=["Authentication"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class FavoriteMovieListCreateView(generics.ListCreateAPIView):
    """
    get:
    Retrieve the list of your favorite movies.
    Requires JWT authentication.
    """
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get a list of your favorite movies.",
        tags=["Favorites"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class AddFavoriteMovieView(APIView):
    """
    post:
    Add a movie to your favorites.
    Requires JWT authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a movie to your favorites list.",
        request_body=AddFavoriteSerializer,
        responses={201: FavoriteMovieSerializer()},
        tags=["Favorites"]
    )
    def post(self, request):
        serializer = AddFavoriteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        return Response(FavoriteMovieSerializer(favorite).data)


class FavoriteMovieDeleteView(APIView):
    """
    delete:
    delete a movie from your favorites.
    Requires JWT authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Remove a movie from your favorites list.",
        manual_parameters=[
            openapi.Parameter(
                "movie_id",
                openapi.IN_PATH,
                description="Movie ID to remove from favorites",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        tags=["Favorites"]
    )

    def delete(self, request, movie_id):
        favorite = FavoriteMovie.objects.filter(user=request.user, movie_id=movie_id).first()
        if not favorite:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)