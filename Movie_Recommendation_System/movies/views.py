from django.shortcuts import render
from django.db.models import Avg, Count
from django.core.cache import cache
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, status,generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import MovieFilter
from .models import Movie
from .services import fetch_trending_movies, fetch_recommendations, TMDBError
from .pagination import LargeResultsSetPagination
from .serializers import TMDbMovieSerializer, MovieSerializer

CACHE_TIMEOUT = getattr(settings, "CACHE_TIMEOUT", 60 * 5)
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

class MovieListCreateView(generics.ListCreateAPIView):
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter  # custom filter
    search_fields = ['title']
    ordering_fields = ['year', 'title']

    @swagger_auto_schema(
        operation_description="Get a list of movies or add a new one. Optionally filter by title, year, tmdb_id.",
        tags=["movies"],
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Filter by release year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
            openapi.Parameter('tmdb_id', openapi.IN_QUERY, description="Filter by TMDb ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request  # Needed for is_favorite
    #     return context
    
    def get_queryset(self):
        cache_key = f"movie_list_{self.request.get_full_path()}"
        cached_qs_ids = cache.get(cache_key)
        if cached_qs_ids is not None:
            return Movie.objects.filter(id__in=cached_qs_ids)

        queryset = Movie.objects.all()

        # Search by title
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title.strip())

        # Filter by tmdb_id (exact)
        tmdb_id = self.request.query_params.get('id')
        if tmdb_id:
            try:
                queryset = queryset.filter(tmdb_id=int(tmdb_id))
            except ValueError:
                return Movie.objects.none()

        # Filter by year (supports comma-separated list)
        year_param = self.request.query_params.get('year')
        if year_param:
            years = []
            for part in year_param.split(','):
                part = part.strip()
                if part.isdigit():
                    years.append(int(part))
            if years:
                if hasattr(Movie, "release_year"):  # if you added release_year field
                    queryset = queryset.filter(release_year__in=years)
                elif hasattr(Movie, "release_date"):  # if you store a DateField
                    queryset = queryset.filter(release_date__year__in=years)

        queryset = queryset.annotate(
            average_rating=Avg('ratings__rating'),
            ratings_count=Count('ratings')
        )

        # Store IDs in cache instead of queryset object
        cache.set(cache_key, list(queryset.values_list('id', flat=True)), CACHE_TIMEOUT)
        return queryset
    
    def perform_create(self, serializer):
        tmdb_id = serializer.validated_data.get('tmdb_id')
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            raise ValidationError({"tmdb_id": "A movie with this TMDb ID already exists."})       
        # Will trigger the Movie model's save() to fetch TMDb details
        serializer.save()

class TrendingMoviesView(APIView):
    # serializer_class = TMDbMovieSerializer
    pagination_class = LargeResultsSetPagination
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
    pagination_class = LargeResultsSetPagination
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

    def get(self, request, movie_id=None):
        title = request.query_params.get("title")

        if not movie_id and not title:
            return Response(
                {"detail": "Please provide either a movie_id in the URL or a title query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If title provided, look up TMDb ID first
        if title and not movie_id:
            search_url = f"{TMDB_BASE_URL}/search/movie"
            params = {"api_key": TMDB_API_KEY, "query": title}
            resp = requests.get(search_url, params=params, timeout=10)

            if resp.status_code != 200 or not resp.json().get("results"):
                return Response(
                    {"detail": "Movie not found on TMDb."},
                    status=status.HTTP_404_NOT_FOUND
                )

            movie_id = resp.json()["results"][0]["id"]

        try:
            movies = fetch_recommendations(movie_id)
        except TMDBError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        serializer = TMDbMovieSerializer(movies, many=True)
        return Response(serializer.data)

        # try:
        #     movies = fetch_recommendations(movie_id)
        # except TMDBError as e:
        #     return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        # serializer = TMDbMovieSerializer(movies, many=True)
        # return Response(serializer.data)

class ClearCacheView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Clear all Redis/Django cache",
        tags=["cache"]
    )
    def post(self, request):
        cache.clear()
        return Response({"message": "Cache cleared successfully"}, status=status.HTTP_200_OK)