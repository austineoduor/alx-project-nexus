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

## 📦 Setup Instructions

### 1️⃣ Clone the repo
```bash
git clone https://github.com/austineoduor/alx-project-nexus.git

cd alx-project-nexus/Movie_Recommendation_System/

## 📜 API Endpoints
**https://alx-project-nexus-production-e3c4.up.railway.app/**

-Movies

*GET /api/movies/trending/ — trending movies*

**GET /api/movies/recommended/ — recommended movies**

## -Users

**POST /api/users/register/ — register user**

*POST /api/users/login/ — get JWT tokens*

*POST /api/users/token/refresh/ — refresh JWT token*

**GET /api/users/favorites/ — list favorites*

**POST /api/users/favorites/ — add favorite*

*DELETE /api/users/favorites/<movie_id>/ — remove favorite*

## -Documentation

*GET /api/docs/ — Swagger UI*

