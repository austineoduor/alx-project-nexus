from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .services import fetch_trending_movies, fetch_recommendations, TMDBError
from .serializers import MovieSerializer

class TrendingMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            movies = fetch_trending_movies()
        except TMDBError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class RecommendedMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, movie_id):
        try:
            movies = fetch_recommendations(movie_id)
        except TMDBError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)