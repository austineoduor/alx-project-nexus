import os
import requests
from django.core.cache import cache

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
CACHE_TIMEOUT = 60 * 60  # 1 hour

class TMDBError(Exception):
    pass

def fetch_trending_movies(media_type='movie', time_window='week'):
    cache_key = f"trending_{media_type}_{time_window}"
    if cached := cache.get(cache_key):
        return cached

    url = f"{TMDB_BASE_URL}/trending/{media_type}/{time_window}"
    params = {"api_key": TMDB_API_KEY}
    resp = requests.get(url, params=params, timeout=10)

    if resp.status_code != 200:
        raise TMDBError(f"TMDb returned status {resp.status_code}")

    data = resp.json().get('results', [])
    cache.set(cache_key, data, CACHE_TIMEOUT)
    return data

def fetch_recommendations(movie_id, page=1):
    cache_key = f"recommendations_{movie_id}_{page}"
    if cached := cache.get(cache_key):
        return cached

    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY, "page": page}
    resp = requests.get(url, params=params, timeout=10)

    if resp.status_code != 200:
        raise TMDBError(f"TMDb returned status {resp.status_code}")

    data = resp.json().get('results', [])
    cache.set(cache_key, data, CACHE_TIMEOUT)
    return data