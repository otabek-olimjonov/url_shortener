from app.core.database import SessionLocal
import app.core.crud as crud
from app.core.celery_config import celery_app

@celery_app.task(name='update_views', bind=True)
def update_views(self, short_key: str):
    db = SessionLocal()
    try:
        crud.increment_views(db, short_key)
    finally:
        db.close()