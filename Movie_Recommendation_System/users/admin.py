from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FavoriteMovie, Watchlist

User = get_user_model()

class FavoriteInline(admin.TabularInline):
    model = FavoriteMovie
    extra = 0
    fields = ('movie', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('movie',)

class WatchlistInline(admin.TabularInline):
    model = Watchlist
    extra = 0
    fields = ('movie', 'added_at')
    readonly_fields = ('added_at',)
    autocomplete_fields = ('movie',)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    inlines = [FavoriteInline, WatchlistInline]