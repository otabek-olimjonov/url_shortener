from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UrlBase(BaseModel):
    url: str

class UrlCreate(UrlBase):
    expiration: Optional[int] = None  # Expiration period in minutes

class ShortUrl(BaseModel):
    url: str
    short_key: str
    created_at: datetime
    expires_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True

class UrlStats(BaseModel):
    url: str
    short_key: str
    views: int
    created_at: datetime
    expires_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True
