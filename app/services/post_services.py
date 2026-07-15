from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.post import PostCreate, PostUpdate
from app.repository.post import post_repo


def create_post(db: Session, post_in: PostCreate, user_id: int):
    return post_repo.create(db= db, obj_in= post_in, author_id=user_id)

def get_posts(db: Session, skip: int = 0, limit: int = 100, search:str = None):
    return post_repo.get_multi(db= db, skip= skip, limit= limit, search=search)

def update_post(db: Session,post_id: int, post_in: PostUpdate, user_id: int):
    post =  post_repo.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # check if the logged-in user is the actual author
    if post.author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post!"
        )
    
    return post_repo.update(db=db, db_obj=post, obj_in=post_in)

def delete_post(db: Session, post_id: int, user_id: int):
    post = post_repo.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check if logged-in user is the actual author
    if post.author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post!"
        )
    post_repo.remove(db=db, db_obj=post)
    return {"message": "Post deleted successfully"}
