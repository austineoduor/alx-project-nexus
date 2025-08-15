from django.db.models import Avg, Count
from rest_framework import serializers
from users.models import FavoriteMovie,MovieRating
from .models import Movie


class TMDbMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    overview = serializers.CharField(allow_blank=True)
    popularity = serializers.FloatField(required=False)
    vote_average = serializers.FloatField(required=False)
    release_date = serializers.CharField(required=False)
    poster_path = serializers.CharField(required=False, allow_null=True)

    swagger_schema_fields = {
        "example": {
            "id": 550,
            "title": "Fight Club",
            "overview": "A depressed man suffering from insomnia meets a strange soap salesman...",
            "popularity": 50.123,
            "vote_average": 8.4,
            "release_date": "1999-10-15",
            "poster_path": "/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg"
        }
    }

class MovieSerializer(serializers.ModelSerializer):
    # is_favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    tmdb_id = serializers.IntegerField(required=False)

    class Meta:
        model = Movie
        fields = [
            "id",
            "tmdb_id",
            "title",
            "poster_url",
            "release_date",
            "year",
            'average_rating',
            'ratings_count',
        ]
    def get_average_rating(self, obj):
        return getattr(obj, "average_rating", None)

    def get_ratings_count(self, obj):
        return getattr(obj, "ratings_count", 0)
    
    def to_internal_value(self, data):
        """
        Override to:
        - Map TMDb 'id' -> tmdb_id
        - Ignore unknown fields
        - Convert poster_path to poster_url
        """
        data = data.copy()

        # Map 'id' to 'tmdb_id'
        if "id" in data and "tmdb_id" not in data:
            data["tmdb_id"] = data.pop("id")

        # Map 'poster_path' to full URL if available
        if "poster_path" in data and "poster_url" not in data:
            data["poster_url"] = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

        # Remove TMDb fields we don't store
        allowed = set(self.fields.keys())  # only keep serializer fields
        filtered_data = {k: v for k, v in data.items() if k in allowed}

        return super().to_internal_value(filtered_data)

    swagger_schema_fields = {
        "example": {
            "id": 1,
            "tmdb_id": 550,
            "title": "Fight Club",
            "poster_url": "https://image.tmdb.org/t/p/w500/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg",
            "release_date": "1999-10-15",
            "year": 1999,
            "average_rating": 4.5,
            "ratings_count": 123
        }
    }
        
class AddFavoriteSerializer(serializers.Serializer):
    tmdb_id = serializers.IntegerField()

    swagger_schema_fields = {
        "example": {
            "tmdb_id": 550
        }
    }