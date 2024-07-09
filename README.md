# URL Shortening Service Documentation

## Overview

This URL shortening service is a robust, scalable application built with FastAPI that provides functionality to shorten long URLs into unique, shorter ones and redirect from the shortened URL to the original URL. The service includes additional features such as URL expiration and usage statistics, with Redis caching and Celery background tasks for improved performance.

## Architecture

The application follows a modular structure:

``` 
    ├── app
    │   ├── core
    │   │   ├── __init__.py
    │   │   ├── celery_config.py
    │   │   ├── crud.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── settings.py
    │   ├── __init__.py
    │   ├── main.py
    │   └── tasks.py
    ├── tests
    │   ├── __init__.py
    │   └── test_main.py
    ├── Dockerfile
    ├── docker-compose.yml
    └── requirements.txt
```

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL (for persistent storage)
- **Cache**: Redis (for improved performance)
- **Task Queue**: Celery (for handling background tasks)
- **Containerization**: Docker

## Core Features

### 1. Create Shortened URL

- **Endpoint**: `POST /shorten`
- **Request Body**: 
  ```python
  class UrlCreate(UrlBase):
      url: str
      expiration: Optional[int] = None  # Expiration period in minutes
  ```
- **Response Body**: 
  ```python
  class ShortUrl(BaseModel):
      url: str
      short_key: str
      created_at: datetime
      expires_at: Optional[datetime]
  ```

This endpoint receives a long URL, generates a unique short key, and stores the mapping in PostgreSQL. Users can optionally specify an expiration time in minutes.

### 2. Redirect to Original URL

- **Endpoint**: `GET /<short_key>`
- **Response**: 
  - If the key exists: Redirects to the original URL (301 status code)
  - If the key doesn't exist or has expired: Returns an error message (404 status code)

### 3. URL Key Expiration

URLs can have an optional expiration time. Expired URLs are automatically removed from the database when accessed.

### 4. Usage Statistics

- **Endpoint**: `GET /stats/<short_key>`
- **Response**:
  ```python
  class UrlStats(BaseModel):
      url: str
      short_key: str
      views: int
      created_at: datetime
      expires_at: Optional[datetime]
  ```

## Database Design

### PostgreSQL Schema

```python
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    short_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    views = Column(Integer, default=0)
```

### Redis Caching

Redis is used to cache frequently accessed URLs, reducing the load on the PostgreSQL database and improving response times.

## Background Tasks

Celery is used to handle background tasks, specifically for updating view counts asynchronously:

```python
@celery_app.task(name='update_views', bind=True)
def update_views(self, short_key: str):
    db = SessionLocal()
    try:
        crud.increment_views(db, short_key)
    finally:
        db.close()
```

This approach allows the main application to remain responsive while view counts are updated in the background.

## Configuration

The application uses Pydantic for configuration management, with separate settings for PostgreSQL and Redis:

```python
class PostgresSettings(BaseSettings):
    # PostgreSQL configuration

class RedisSettings(BaseSettings):
    # Redis configuration
```

These settings are loaded from environment variables or a `.env` file.

## Database Operations

Key database operations are handled in the `crud.py` file:

- `create_url`: Creates a new shortened URL
- `get_url`: Retrieves a URL by its short key, handling expiration
- `get_url_stats`: Retrieves statistics for a URL
- `increment_views`: Increments the view count for a URL

## Scalability and Performance Considerations

- Redis caching improves performance by reducing database queries for frequently accessed URLs.
- Celery background tasks ensure that view count updates don't slow down the main application.
- The combination of PostgreSQL for persistent storage and Redis for caching allows for efficient scaling of read and write operations.

## Security Measures

- Input validation using Pydantic models
- Secure generation of short keys using a combination of letters and digits
- Automatic expiration of URLs to manage database growth

## Future Improvements

- Implement a cleanup task for expired URLs that haven't been accessed
- Add more detailed analytics for URL usage
- Implement rate limiting to prevent abuse of the service

## Testing

The `tests` directory contains unit tests and integration tests. Ensure to add tests for the new Redis caching and Celery task functionalities.

## Deployment

Use the provided `Dockerfile` and `docker-compose.yml` for building and running the application. Ensure that the necessary environment variables are set for PostgreSQL, Redis, and Celery configurations.