import requests
from django.conf import settings

TMDB_API_BASE = "https://api.themoviedb.org/3"

def fetch_tmdb_movie_details(tmdb_id):
    """
    Fetches movie details from TMDb API by tmdb_id.
    Returns a dict with 'release_date' and 'poster_url'.
    """
    headers = {
        "Authorization": f"Bearer {settings.TMDB_API_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }
    url = f"{TMDB_API_BASE}/movie/{tmdb_id}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "release_date": data.get("release_date"),
            "poster_url": f"https://image.tmdb.org/t/p/w500{data.get('poster_url')}" if data.get("poster_path") else None
        }
    else:
        return None