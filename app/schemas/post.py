from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# foundation
class PostBase(BaseModel):
    title: str
    content: str

# creation schema
class PostCreate(PostBase):
    pass 

# update schema
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# response schema
class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
