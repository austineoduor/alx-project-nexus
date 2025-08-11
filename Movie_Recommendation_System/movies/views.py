from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import fetch_trending_movies, fetch_recommendations, TMDBError
from .serializers import TMDbMovieSerializer, MovieSerializer

class TrendingMoviesView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_description="Retrieve the current trending movies from TMDb (cached in Redis for performance).",
        responses={200: MovieSerializer(many=True)},
        tags=["Movies"]
    )
    def get(self, request):
        try:
            movies = fetch_trending_movies()
        except TMDBError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        serializer = TMDbMovieSerializer(movies, many=True)
        return Response(serializer.data)

class RecommendedMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve movie recommendations for a given TMDb movie ID (cached in Redis).",
        manual_parameters=[
            openapi.Parameter(
                'movie_id',
                openapi.IN_QUERY,
                description="TMDb movie ID for which to fetch recommendations",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: MovieSerializer(many=True)},
        tags=["Movies"]
    )

    def get(self, request, movie_id):
        try:
            movies = fetch_recommendations(movie_id)
        except TMDBError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        serializer = TMDbMovieSerializer(movies, many=True)
        return Response(serializer.data)