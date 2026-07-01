import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = str(os.getenv("DATABASE_URL"))
    SENDER_EMAIL = str(os.getenv("SENDER_EMAIL"))
    EMAIL_APP_PASSWORD = str(os.getenv("EMAIL_APP_PASSWORD"))


settings = Settings()