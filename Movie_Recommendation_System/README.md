# 🎬 Movie Recommendation Backend

A Django + DRF backend for a movie recommendation app, integrating TMDb API for trending/recommended movies, JWT authentication, Redis caching, and Swagger documentation.

## 🚀 Features
- **Trending & Recommended Movies** — via TMDb API
- **User Authentication** — JWT-based (register, login, refresh)
- **Favorites Management** — save/remove favorite movies
- **Performance Optimization** — Redis caching
- **API Documentation** — Swagger UI at `/api/docs/`

## 🛠 Technologies
- Django + Django REST Framework
- PostgreSQL
- Redis (via `django-redis`)
- TMDb API
- drf-yasg (Swagger)

### Explore the hosted backend
    ** copy and paste on a browser
    [URL: ](https://alx-project-nexus-production-e3c4.up.railway.app/)
    
## Quick test flow (curl)
    Register


    curl -X POST https://127.0.0.1;8080/api/users/register/ \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","email":"a@example.com","password":"secret123"}'

## To Obtain tokens (login)

    curl -X POST https://127.0.0.1;8080/api/users/token/ \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"secret123"}'
    
    - Response contains:
        {"access":"<ACCESS_TOKEN>", "refresh":"<REFRESH_TOKEN>"}

## Call protected endpoint

    curl -X GET https://<your-host>/api/users/favorites/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"

## Refresh access token
    curl -X POST https://<your-host>/api/users/token/refresh/ \
    -H "Content-Type: application/json" \
    -d '{"refresh":"<REFRESH_TOKEN>"}'

## 📦 Setup Instructions

### 1️⃣ Clone the repo

```bash

git clone https://github.com/austineoduor/alx-project-nexus.git

cd alx-project-nexus/Movie_Recommendation_System/

## 📜 API Endpoints

-Movies

    GET /api/movies/trending/  →  trending movies
    GET /api/movies/recommended/  → recommended movies

    GET /api/movies/?title=matrix
    GET /api/movies/?tmdb_id=550
    GET /api/movies/?year=1999
    GET /api/movies/?year=2022,2023
    GET /api/movies/?title=man&tmdb_id=56789

-Users

    POST /api/users/register/  →  register user
    POST /api/users/login/  → get JWT tokens
    POST /api/users/token/refresh/  →  refresh JWT token
    POST /api/users/favorites/  →  add favorite
    POST /api/movies/rate/  →   One rating per movie per user (updates instead of duplicates)
    GET /api/favorites/?title=man → Favorites containing “man” in the title.
    GET /api/favorites/?tmdb_id=12345 → Favorites for a specific movie.
    GET /api/users/favorites/  →  list favorites
    
    DELETE /api/users/favorites/<movie_id>/ →  remove favorite

-Documentation

    GET /api/docs/  →  Swagger UI
    GET /api/redoc/  → redoc UI
