from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services import post_services

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_new_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_services.create_post(db=db, post_in=post_in, user_id=current_user.id)

@router.get("/", response_model=List[PostResponse])
def read_all_posts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),

):
    return post_services.get_posts(db=db, skip=skip, limit=limit, search=search)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_services.update_post(db=db, post_id=post_id, post_in=post_in, user_id=current_user.id)

@router.delete("/{post_id}")
def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_services.delete_post(db=db, post_id=post_id, user_id=current_user.id)

