import requests
from django.core.cache import cache
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_API_BASE = "https://api.themoviedb.org/3"
CACHE_TIMEOUT = 60 * 60

class TMDBError(Exception):
    pass

def fetch_tmdb_movie_details(tmdbid):
    """
    Fetches movie details from TMDb API by tmdb_id.
    Returns a dict with 'release_date' and 'poster_url'.
    """
    tmdb_id = int(tmdbid)
    cache_key = f"movie_details_{tmdb_id}"
    if cached := cache.get(cache_key):
        return cached
    
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "Content-Type": "application/json;charset=utf-8"
    }
    
    url = f"{TMDB_API_BASE}/movie/{tmdb_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = {
                "release_date": data.get("release_date"),
                "poster_url": f"https://image.tmdb.org/t/p/w500{data.get('poster_url')}" if data.get("poster_path") else None
            }
            cache.set(cache_key, result, CACHE_TIMEOUT)
            return result
    except Exception.TMDBError as e:
        return (f"TMDb returned status {response.status_code} for movie {tmdb_id}: {e}")
        # return None