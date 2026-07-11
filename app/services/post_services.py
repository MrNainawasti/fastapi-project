from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.post import PostCreate, PostUpdate
from app.crud import post as crud_post

def create_post(db: Session, post_in: PostCreate, user_id: int):
    return crud_post.create(db= db, post_in= post_in, author_id=user_id)

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return crud_post.get_multi(db= db, skip= skip, limit= limit)

def update_post(db: Session,post_id: int, post_in: PostUpdate, user_id: int):
    post =  crud_post.get(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # check if the logged-in user is the actual author
    if post.author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post!"
        )
    
    return crud_post.update(db=db, db_post=post, post_in=post_in)

def delete_post(db: Session, post_id: int, user_id: int):
    post = crud_post.get(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check if logged-in user is the actual author
    if post.author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post!"
        )
    crud_post.remove(db=db, db_post=post)
    return {"message": "Post deleted successfully"}
