from rest_framework import serializers
from .models import FavoriteMovie, User
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
        fields = ['favoritemovie_id', 'movie_id', 'title', 
                  'poster_path', 'added_at']
        read_only_fields = fields