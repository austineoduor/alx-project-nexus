import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from movies.models import Movie
from rest_framework import serializers
from .models import( FavoriteMovie, User,
                    MovieRating, FavoriteActivity,
                    Watchlist)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"first_name","last_name",
                  "phone_number", 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'phone_number',
                  'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    swagger_schema_fields = {
        "example": {
            'username': 'john_doe',
            'first_name': 'john',
            'last_name': 'doe',
            'phone_number': '+16044011234',
            'email': 'john@example.com',
            'password': 'securepassword123'
        }
    }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ['id', 'movie', 'updated_at']
        read_only_fields = fields

    swagger_schema_fields = {
        "example": {
            "id": "1",
            "tmdb_id": 550,
            "added_at": "2025-08-11T15:30:00Z"
        }
    }


class AddFavoriteSerializer(serializers.Serializer):
    tmdb_id = serializers.IntegerField()
    class Meta:
        model = FavoriteMovie
        fields = ["tmdb_id",]

    swagger_schema_fields = {
        "example": {
            "tmdb_id": 550,
        }
    }

    def to_internal_value(self, data):
        data = data.copy()
        if "id" in data and "tmdb_id" not in data:
            data["tmdb_id"] = data.pop("id")
        else:
            raise serializers.ValidationError({"tmdb_id": "This field is required."})
        
        allowed = set(self.fields.keys())  # keep only declared fields
        filtered_data = {k: v for k, v in data.items() if k in allowed}
        return super().to_internal_value(filtered_data)

    def create(self, validated_data):
        user = self.context["request"].user
        tmdb_id = validated_data["tmdb_id"]

        # Create or get the movie first
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
        )

        # Create favorite link
        favorite, _ = FavoriteMovie.objects.get_or_create(user=user, movie=movie)
        return favorite
    
    
class MovieRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5, help_text="Rating from 1 to 5 stars")
    movie = serializers.StringRelatedField(read_only=True)
    tmdb_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieRating
        fields = ['tmdb_id', 'rating', 'movie']

    def validate(self, attrs):
        tmdb_id = attrs.pop('movie', None)
        if tmdb_id is None:
            raise serializers.ValidationError({"movie": "This field is required."})

        movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
        attrs['movie'] = movie
        return attrs
            
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class FavoriteActivitySerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)

    class Meta:
        model = FavoriteActivity
        fields = ['movie_title', 'action', 'timestamp']


class WatchlistSerializer(serializers.ModelSerializer):
    tmdb_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'tmdb_id', 'added_at']
        read_only_fields = ['id', 'movie', 'added_at']

    def to_internal_value(self, data):
        data = data.copy()
        if "id" in data and "tmdb_id" not in data:
            data["tmdb_id"] = data.pop("id")
        else:
            raise serializers.ValidationError({"tmdb_id": "This field is required."})
        
        allowed = set(self.fields.keys())  # keep only declared fields
        filtered_data = {k: v for k, v in data.items() if k in allowed}
        return super().to_internal_value(filtered_data)

    def create(self, validated_data):
        user = self.context["request"].user
        tmdb_id = validated_data["tmdb_id"]

        # Create or get the movie first
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
        )
        # Create the watchlist entry
        watchlist, _ = Watchlist.objects.get_or_create(user=user, movie=movie)
        return watchlist