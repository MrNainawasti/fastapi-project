from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def get(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def create(db: Session, post_in: PostCreate, author_id: int):
    db_post = Post(**post_in.model_dump(), author_id = author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update(db: Session, db_post: Post, post_in: PostUpdate):
    update_data = post_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def remove(db: Session, db_post: Post):
    db.delete(db_post)
    db.commit()
    return db_post

