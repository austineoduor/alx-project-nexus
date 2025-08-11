from rest_framework import serializers
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
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "title", "poster_url"]
        
    swagger_schema_fields = {
        "example": {
            "id": 1,
            "tmdb_id": 550,
            "title": "Fight Club",
            "poster_url": "/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg"
        }
    }
        
class AddFavoriteSerializer(serializers.Serializer):
    tmdb_id = serializers.IntegerField()

    swagger_schema_fields = {
        "example": {
            "tmdb_id": 550
        }
    }