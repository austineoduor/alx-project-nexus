from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True )
    title = models.CharField(max_length=255, null=True)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title