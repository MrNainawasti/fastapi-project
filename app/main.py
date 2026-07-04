from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.database import Base, engine

TITLE = "AUTH API"
WELCOME_MESSAGE = "Welcome to Auth API"

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=TITLE)

app.include_router(api_router, prefix="/api/v1")

app.get("/")
def root():
    return{
        "message": WELCOME_MESSAGE
    }
