from pydantic import BaseModel
from typing import Optional
from schemas.address import Address

class CachedResponse(BaseModel):
    is_cached: bool
    data: Optional[dict | str] = None