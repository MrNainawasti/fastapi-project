from app.repository.base import BaseRepository
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    pass

post_repo = PostRepository(Post)

