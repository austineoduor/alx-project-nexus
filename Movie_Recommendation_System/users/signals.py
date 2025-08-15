from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .views import FavoriteMovieListView
from .models import FavoriteMovie, FavoriteActivity

@receiver(post_save, sender=FavoriteMovie)
@receiver(post_delete, sender=FavoriteMovie)
def clear_favorites_cache(sender, instance, **kwargs):
    FavoriteMovieListView.invalidate_user_cache(instance.user.id)

@receiver(post_save, sender=FavoriteMovie)
def log_favorite_added(sender, instance, created, **kwargs):
    if created:
        FavoriteActivity.objects.create(
            user=instance.user,
            movie=instance.movie,
            action='added'
        )

@receiver(post_delete, sender=FavoriteMovie)
def log_favorite_removed(sender, instance, **kwargs):
    FavoriteActivity.objects.create(
        user=instance.user,
        movie=instance.movie,
        action='removed'
    )