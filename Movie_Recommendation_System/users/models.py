from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()

class FavoriteMovie(models.Model):
    favoritemovie_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False
        )
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_id')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.title} ({self.movie_id})"
