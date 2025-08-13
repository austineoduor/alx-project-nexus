import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    year = django_filters.CharFilter(method='filter_year')

    def filter_year(self, queryset, name, value):
        """
        Accepts comma-separated years, e.g., ?year=2022,2023
        """
        years = [y.strip() for y in value.split(',') if y.strip().isdigit()]
        return queryset.filter(year__in=years)

    class Meta:
        model = Movie
        fields = ['year']