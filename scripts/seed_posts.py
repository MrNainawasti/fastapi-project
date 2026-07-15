import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

sys.path.append(project_root)

from app.db.database import SessionLocal
from app.models.post import Post
from app.models.user import User



def run_seed():
    db = SessionLocal()

    try:
        # check if atleast one user exists in database
        user = db.query(User).first()
        if not user:
            print("Error: No user found. Create atleast one user.")
            return
        
        print("Starting seeding process...")
        # creating 100,000 posts
        posts_to_insert = []
        for i in range(1, 100001):
            new_post = Post(
                title = f"Dummy Post Number {i}",
                content = f"This is automatic dummy content for post {i}.",
                author_id = user.id
            )
            posts_to_insert.append(new_post)

            # inserting batches  of 10,000 records 
            if i % 10000 == 0:
                db.bulk_save_objects(posts_to_insert)
                db.commit()
                posts_to_insert.clear()
                print(f"Inserted {i} records so far...")

        print("Success! 100,000 dummy posts have been seeded into database.")

    except Exception as e:
        print(f"An error occured: {e}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

