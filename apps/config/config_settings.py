from pydantic_settings import BaseSettings
from functools import lru_cache

class AppSettings(BaseSettings):
    # FastAPI Configuration
    title: str = "Mongo DB With FAST API and Firebase"
    debug: bool = True  # Set to True for development, False for production
    host: str = "0.0.0.0"
    port: int = 8000

    # Firebase Configuration
    firebase_api_key: str
    firebase_auth_domain: str
    firebase_project_id: str
    firebase_storage_bucket: str
    firebase_messaging_sender_id: str
    firebase_app_id: str
    firebase_measurement_id : str

    FIREBASE_ADMIN_CREDENTIALS: str
    # MongoDB Configuration
    mongodb_uri: str
    mongodb_database: str
    mongodb_collection: str

    class Config:
        env_file = ".env"  # Load configuration from the .env file

@lru_cache()
def get_settings():
    return AppSettings()


settings = get_settings()