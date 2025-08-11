from rest_framework import serializers
from .models import FavoriteMovie, User
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
        fields = ['favoritemovie_id', 'movie', 'title', 
                  'poster_path', 'added_at']
        read_only_fields = fields

    swagger_schema_fields = {
        "example": {
            "favoritemovie_id": "b3a3c2f8-ccf6-4a83-bad5-bd1f6f6c2c99",
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