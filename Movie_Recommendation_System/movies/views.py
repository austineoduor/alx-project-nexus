from django.shortcuts import render
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status,generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import MovieFilter
from .models import Movie
from .services import fetch_trending_movies, fetch_recommendations, TMDBError
from .serializers import TMDbMovieSerializer, MovieSerializer

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter  # custom filter
    search_fields = ['title']
    ordering_fields = ['year', 'title']

    @swagger_auto_schema(
        operation_description="Get a list of movies. Optionally filter by year using ?year=YYYY",
        tags=["movies"],
        manual_parameters=[
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="Filter movies by release year (e.g. ?year=2023)",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request  # Needed for is_favorite
    #     return context
    
    def get_queryset(self):
        queryset = Movie.objects.all()

        # Search by title
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Filter by tmdb_id
        tmdb_id = self.request.query_params.get('tmdb_id')
        if tmdb_id:
            queryset = queryset.filter(tmdb_id=tmdb_id)

        # Optional: filter by year (if we add year field later)
        year = self.request.query_params.get('year')
        if year and queryset.model._meta.get_field('release_date'):
            queryset = queryset.filter(release_date__year=year)
            
        queryset = queryset.annotate(
            average_rating=Avg('ratings__rating'),
            ratings_count=Count('ratings')
            )

        return queryset

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