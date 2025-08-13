import django_filters
from .models import FavoriteMovie

class FavoriteMovieFilter(django_filters.FilterSet):
    # Partial title match
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    # Filter by TMDB ID (from related Movie model)
    tmdb_id = django_filters.NumberFilter(field_name="movie__tmdb_id", lookup_expr="exact")

    class Meta:
        model = FavoriteMovie
        fields = ["title", "tmdb_id"]