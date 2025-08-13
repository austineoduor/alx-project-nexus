from rest_framework import serializers
from .models import FavoriteMovie, User, MovieRating
from movies.models import Movie
import uuid
from django.contrib.auth import get_user_model

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
        fields = ['id', 'movie', 'title', 
                  'poster_path', 'updated_at']
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
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True, allow_null=True)
    poster_path = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = FavoriteMovie
        fields = ["tmdb_id"]

    swagger_schema_fields = {
        "example": {
            "tmdb_id": 550
        }
    }
    
    def create(self, validated_data):
        user = self.context["request"].user
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=validated_data["tmdb_id"],
            defaults={
                "title": validated_data["title"],
                "overview": validated_data["overview"],
                "poster_path": validated_data.get("poster_path"),
            },
        )
        favorite, created = FavoriteMovie.objects.get_or_create(user=user, movie=movie)
        return favorite
    
class MovieRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5, help_text="Rating from 1 to 5 stars")
    
    class Meta:
        model = MovieRating
        fields = ['user','movie', 'rating', 'created_at','updated_at']
        read_only_fields = ['user','movie', 'created_at','updated_at']
        
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value