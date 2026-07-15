from sqlalchemy.orm import Session
from sqlalchemy import or_ 
from app.repository.base import BaseRepository
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate



class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):

    # redefine get_multi to accept optional search string
    def get_multi(self, db:Session, *, skip:int = 0, limit:int = 100, search:str = None):
        query = db.query(self.model)

        # filter the results according to search term, before paginating
        if search:
            query = query.filter(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    self.model.content.ilike(f"%{search}%")
                )
            )

        return query.offset(skip).limit(limit).all()

post_repo = PostRepository(Post)

