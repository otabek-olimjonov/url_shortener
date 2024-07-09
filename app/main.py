from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import app.core.crud as crud
import app.core.models as models
import app.core.schemas as schemas
from app.core.database import engine, redis_client, get_db
from app.core.celery_config import celery_app

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def update_views(db: Session, short_key: str):
    crud.increment_views(db, short_key)

@app.post("/shorten", response_model=schemas.ShortUrl)
def create_short_key(url: schemas.UrlCreate, db: Session = Depends(get_db)):
    db_url = crud.create_url(db, url)
    redis_client.set(db_url.short_key, db_url.url)
    return db_url

@app.get("/{short_key}")
def redirect_to_url(short_key: str, db: Session = Depends(get_db)):
    # Check cache first
    cached_url = redis_client.get(short_key)

    if cached_url:
        celery_app.send_task("update_views", args=[short_key], kwargs={}, queue='tasks')
        return RedirectResponse(url=cached_url.decode(), status_code=301)

    db_url = crud.get_url(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found or expired")
    
    # Update cache
    redis_client.set(short_key, db_url.url)
    return RedirectResponse(url=db_url.url, status_code=301)

@app.get("/stats/{short_key}", response_model=schemas.UrlStats)
def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_stats(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url
