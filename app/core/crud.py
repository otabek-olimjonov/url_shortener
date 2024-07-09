from sqlalchemy.orm import Session
import string
import random
import datetime
import app.core.models as models
import app.core.schemas as schemas

def generate_short_key(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_url(db: Session, url: schemas.UrlCreate):
    short_key = generate_short_key()
    expires_at = None
    if url.expiration:
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=url.expiration)
    db_url = models.URL(
        url=url.url,
        short_key=short_key,
        expires_at=expires_at
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db: Session, short_key: str):
    db_url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if db_url and db_url.expires_at and db_url.expires_at < datetime.datetime.utcnow():
        db.delete(db_url)
        db.commit()
        return None
    if db_url:
        db_url.views += 1
        db.commit()
    return db_url

def get_url_stats(db: Session, short_key: str):
    return db.query(models.URL).filter(models.URL.short_key == short_key).first()

def increment_views(db: Session, short_key: str):
    db_url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if db_url:
        db_url.views += 1
        db.commit()
