from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from movies.models import Movie

class User(AbstractUser):
    first_name = models.CharField(
        max_length=100,
        help_text="Allowed Letters, digits and @/./+/-/_ only.")
    last_name = models.CharField(
        max_length=100,
        help_text="Allowed Letters, digits and @/./+/-/_ only.")
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Format: +16044011234")

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True,)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
class MovieRating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 stars
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} - {self.rating}★"
