from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .filters import FavoriteMovieFilter
from .models import FavoriteMovie,MovieRating
from .serializers import (RegisterSerializer,
                          AddFavoriteSerializer,
                          FavoriteMovieSerializer,
                          MovieRatingSerializer)

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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


class FavoriteMovieListView(generics.ListAPIView):
    """
    List a user's favorite movies with optional filtering.
    """
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FavoriteMovieFilter
    search_fields = ["title"]
    ordering_fields = ["title", "added_at"]

    def get_queryset(self):
        # Only return the authenticated user's favorites
        return FavoriteMovie.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get favorite movies. Optional filtering by title or TMDB ID.",
        tags=["movies"],
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_QUERY, description="Partial favorite movie title", type=openapi.TYPE_STRING),
            openapi.Parameter("tmdb_id", openapi.IN_QUERY, description="Exact TMDB ID of the movie", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
    

class RateMovieView(generics.CreateAPIView):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]



    @swagger_auto_schema(
        operation_description="Rate a movie between 1 and 5 stars. Updates if rating exists.",
        responses={
            200: openapi.Response(
                description="Rating saved successfully",
                examples={
                    "application/json": {
                        "message": "Rating saved successfully",
                        "average_rating": 4.3,
                        "ratings_count": 15
                    }
                }
            ),
            400: "Invalid data",
            401: "Authentication required"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = serializer.validated_data['movie']
        rating = serializer.validated_data['rating']

        # Update or create rating
        MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating}
        )

        # Calculate new stars
        stars = MovieRating.objects.filter(movie=movie).aggregate(
            average_rating=Avg('rating'),
            ratings_count=Count('id')
        )

        return Response({
            "message": "Rating saved successfully",
            "average_rating": round(stars['average_rating'], 2) if stars['average_rating'] else None,
            "ratings_count": stars['ratings_count']
        }, status=status.HTTP_200_OK)

    #     # serializer.save(user=self.request.user)
