from django.contrib import admin
from django.db.models import Avg, Count
from users.models import MovieRating
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'tmdb_id', 'average_rating', 'ratings_count')
    search_fields = ('title', 'tmdb_id')
    list_filter = ('release_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            avg_rating=Avg('ratings__rating'),
            rating_count=Count('ratings')
        )

    def average_rating(self, obj):
        return round(obj.avg_rating or 0, 2)
    average_rating.short_description = 'Average Rating'

    def ratings_count(self, obj):
        return obj.rating_count
    ratings_count.short_description = 'Ratings Count'


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at', 'updated_at')
    search_fields = ('movie__title', 'user__username')
    list_filter = ('rating', 'created_at', 'updated_at')