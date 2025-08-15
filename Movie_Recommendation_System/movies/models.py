from django.db import models
from .utils import fetch_tmdb_movie_details

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_url = models.URLField(blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-fetch details from TMDb if missing
        if not self.release_date or not self.poster_url:
            details = fetch_tmdb_movie_details(self.tmdb_id)
            if details:
                if not self.release_date and details["release_date"]:
                    self.release_date = details["release_date"]
                if not self.poster_url and details["poster_url"]:
                    self.poster_url = details["poster_url"]

        # Auto-set year based on release_date
        if self.release_date:
            self.year = self.release_date.year
        super().save(*args, **kwargs)
        class Meta:
            unique_together = ('tmdb_id', 'title')
            ordering = ['-year']
        def __str__(self):
            return self.title