from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.database import Base, engine

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API")

app.include_router(api_router, prefix="/api/v1")

app.get("/")
def root():
    return{
        "message": "Welcome to Aut API"
    }
