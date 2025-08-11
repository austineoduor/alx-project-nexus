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
    # favoritemovie_id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True, 
    #     editable=False
    #     )
    user = models.ForeignKey(User, related_name='favorites',null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
